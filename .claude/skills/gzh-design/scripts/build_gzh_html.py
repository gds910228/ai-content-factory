#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_gzh_html.py — 把本地配图带入公众号预览 HTML，产出相对路径版 + base64 自包含版。

铁律（见 references/image-embed.md）：绝不让 LLM 在 HTML 里手写 base64——
N 张图转 base64 是数 MB 纯文本，会撑爆 LLM 输出 token、API 返回 400、会话崩溃。
base64 编码由本脚本本地完成，LLM 只写 <img src="imgs/x.png">。

输入：
  --src      预览 HTML（wrap_preview.py 产出的 _预览.html；含 2c 占位框或已有 <img src="imgs/...">）
  --imgs     配图目录
  --spec     可选 JSON，声明每张图放哪（占位框模式）
  --out-dir  可选，默认与 src 同目录
  --theme    可选主题英文标识(如 red-white)，从 references/theme-{id}.md 读主色套到图片框(主色淡边+淡主色影)

spec.json：
  [
    {"op":"replace","anchor":"占位框唯一文本","file":"01.png","alt":"图说","caption":"图1｜..."},
    {"op":"insert", "anchor":"段落唯一一句","file":"02.png","alt":"图说","caption":"图2｜..."}
  ]
  op=replace 替换含 anchor 的 <section>...</section>；op=insert 在含 anchor 的 </p> 后插入。
  caption 可空（空则不加说明 <p>，符合"不硬造说明"）。

输出：
  <stem>_含图.html          相对路径 imgs/<file>（首选，须与 imgs/ 同目录）
  <stem>_含图_自包含.html    base64 内嵌（兜底，单文件可移植）

用法：
  python build_gzh_html.py --src "X_预览.html" --imgs "imgs" --spec "spec.json"
  python build_gzh_html.py --src "X_预览.html" --imgs "imgs"   # 只转 base64，不占位
"""
import argparse
import base64
import json
import os
import re
import sys

# Windows 控制台默认 GBK，打印 emoji 会崩；强制 stdout utf-8 + 容错
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "gif": "image/gif", "webp": "image/webp", "svg": "image/svg+xml"}


def data_uri(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    return "data:{0};base64,{1}".format(MIME.get(ext, "image/png"), b64)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def parse_theme_vars(text):
    """从主题文件「设计变量速查表」解析 {标签: #hex}，兼容各主题命名差异。"""
    out = {}
    for line in text.splitlines():
        m = re.match(r'^\s*([^:：\n]+?)[:：]\s*(#[0-9A-Fa-f]{6})', line)
        if m:
            out[m.group(1).strip()] = m.group(2)
    return out


def pick_theme_colors(vars_):
    """从变量表挑图片框用的 主色 / 边框色 / 说明色（带兜底）。"""
    primary = None
    for k, v in vars_.items():
        if "主色" in k and not any(x in k for x in ("深", "浅", "背景", "极")):
            primary = v
            break
    if not primary:
        for k, v in vars_.items():
            if "主色" in k:
                primary = v
                break
    border = None
    for kw in ("极浅", "浅标", "标记", "浅底", "背景"):
        for k, v in vars_.items():
            if kw in k:
                border = v
                break
        if border:
            break
    if not border:
        border = vars_.get("分割线色") or "#E5E7EB"
    caption = vars_.get("辅助文字色") or "#9CA3AF"
    return primary, border, caption


def img_section(src, alt, caption, colors=None):
    """2a 图片组件：白底卡片 + 居中 img + 可选说明。<span leaf> 包裹，过校验。
    colors=None 用中性默认(多数主题图片框本就中性)；传 --theme 解析结果则套主色为强调变体。"""
    alt = alt or ""
    if colors:
        border = colors["border"]
        shadow = "0 4px 12px -2px rgba({0},0.18)".format(colors["shadow_rgb"])
        cap_color = colors["caption"]
    else:
        border = "#E5E7EB"
        shadow = "0 4px 12px -2px rgba(0,0,0,0.08)"
        cap_color = "#9CA3AF"
    card = (
        '<section style="background:#FFF;border-radius:12px;padding:6px;'
        'border:1px solid {bd};box-shadow:{sh};margin:8px 0 {mb};">'
        '<span leaf=""><img src="{src}" alt="{alt}" '
        'style="max-width:100%;height:auto;display:block;margin:0 auto;" /></span>'
        '</section>'
    )
    if caption:
        cap = (
            '<p style="font-size:12px;color:{cc};text-align:center;margin:0 0 24px;">'
            '<span leaf="">- {cap}</span></p>'
        )
        return card.format(bd=border, sh=shadow, mb="8px", src=src, alt=alt) + cap.format(cc=cap_color, cap=caption)
    return card.format(bd=border, sh=shadow, mb="24px", src=src, alt=alt)


def replace_placeholder(html, anchor, section_html):
    """替换包含 anchor 文本的最近一个 <section>...</section>（2c 占位框）。"""
    i = html.find(anchor)
    if i < 0:
        sys.exit("❌ replace: 找不到锚点文本: " + anchor)
    start = html.rfind("<section", 0, i)
    end = html.find("</section>", i)
    if start < 0 or end < 0:
        sys.exit("❌ replace: 锚点不在 <section> 内（确认是占位框?）: " + anchor)
    return html[:start] + section_html + html[end + len("</section>"):]


def insert_after_p(html, anchor, section_html):
    """在包含 anchor 文本的最近一个 <p>...</p> 之后插入。"""
    i = html.find(anchor)
    if i < 0:
        sys.exit("❌ insert: 找不到锚点文本: " + anchor)
    end = html.find("</p>", i)
    if end < 0:
        sys.exit("❌ insert: 找不到锚点 </p>: " + anchor)
    end += len("</p>")
    return html[:end] + "\n" + section_html + html[end:]


def resolve_local(src, imgs_dir):
    """src 指向 imgs_dir 内的本地文件则返回绝对路径，否则 None（http/data 等跳过）。"""
    s = src.strip()
    if s.startswith(("data:", "http://", "https://", "file://")):
        return None
    norm = s.lstrip("./")
    cands = [os.path.join(imgs_dir, norm)]
    if norm.startswith("imgs/"):
        cands.append(os.path.join(imgs_dir, norm[4:]))
    cands.append(os.path.join(imgs_dir, os.path.basename(norm)))
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


IMG_RE = re.compile(r'(<img\b[^>]*?\bsrc=)(["\'])([^"\']+)(\2[^>]*>)', re.I)


def embed_local_images(html, imgs_dir):
    """把所有指向本地 imgs 的 <img src> 换成 data-URI；http/data 等保持不变。"""
    def repl(m):
        pre, q, src, post = m.group(1), m.group(2), m.group(3), m.group(4)
        path = resolve_local(src, imgs_dir)
        if path:
            return pre + q + data_uri(path) + post
        return m.group(0)
    return IMG_RE.sub(repl, html)


def main():
    ap = argparse.ArgumentParser(description="本地配图带入公众号预览 HTML")
    ap.add_argument("--src", required=True, help="预览 HTML 路径")
    ap.add_argument("--imgs", required=True, help="配图目录")
    ap.add_argument("--spec", default=None, help="可选 JSON 配置（占位框模式）")
    ap.add_argument("--out-dir", default=None, help="输出目录（默认与 src 同目录）")
    ap.add_argument("--theme", default=None, help="主题英文标识(如 red-white)，从 references/theme-{id}.md 读主色套到图片框")
    args = ap.parse_args()

    src = os.path.abspath(args.src)
    imgs_dir = os.path.abspath(args.imgs)
    out_dir = args.out_dir or os.path.dirname(src)
    if not os.path.isfile(src):
        sys.exit("❌ 源 HTML 不存在: " + src)
    if not os.path.isdir(imgs_dir):
        sys.exit("❌ 配图目录不存在: " + imgs_dir)

    colors = None
    if args.theme:
        theme_md = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "references", "theme-{0}.md".format(args.theme))
        if not os.path.isfile(theme_md):
            sys.exit("❌ 主题文件不存在: " + theme_md + "（检查 --theme 标识）")
        vars_ = parse_theme_vars(open(theme_md, encoding="utf-8").read())
        primary, border, cap = pick_theme_colors(vars_)
        if not primary:
            sys.exit("❌ 主题文件未解析到主色: " + theme_md)
        r, g, b = hex_to_rgb(primary)
        colors = {"border": border,
                  "shadow_rgb": "{0},{1},{2}".format(r, g, b),
                  "caption": cap}
        print("🎨 主题套色({0}): 主色 {1} -> 边框 {2}, 阴影 rgba({3},0.18), 说明色 {4}".format(
            args.theme, primary, border, colors["shadow_rgb"], cap))

    with open(src, encoding="utf-8") as f:
        html = f.read()

    n_placed = 0
    if args.spec:
        with open(os.path.abspath(args.spec), encoding="utf-8") as f:
            specs = json.load(f)
        if not isinstance(specs, list) or not specs:
            sys.exit("❌ spec 必须是非空 JSON 数组")
        for s in specs:
            for k in ("op", "anchor", "file"):
                if k not in s:
                    sys.exit("❌ spec 项缺字段 " + k)
            p = os.path.join(imgs_dir, s["file"])
            if not os.path.isfile(p):
                sys.exit("❌ 配图不存在: " + p)
            sec = img_section("imgs/" + s["file"], s.get("alt", ""), s.get("caption", ""), colors)
            if s["op"] == "replace":
                html = replace_placeholder(html, s["anchor"], sec)
            elif s["op"] == "insert":
                html = insert_after_p(html, s["anchor"], sec)
            else:
                sys.exit("❌ op 只能是 replace/insert: " + str(s["op"]))
            n_placed += 1

    html_rel = html
    html_b64 = embed_local_images(html_rel, imgs_dir)
    n_embedded = html_b64.count("data:image") - html_rel.count("data:image")

    stem = os.path.splitext(os.path.basename(src))[0]
    rel_out = os.path.join(out_dir, stem + "_含图.html")
    b64_out = os.path.join(out_dir, stem + "_含图_自包含.html")
    with open(rel_out, "w", encoding="utf-8") as f:
        f.write(html_rel)
    with open(b64_out, "w", encoding="utf-8") as f:
        f.write(html_b64)

    mode = "占位注入 {0} 张".format(n_placed) if args.spec else "仅转 base64"
    print("✅ 完成（{0}，嵌入 {1} 张为 data-URI）".format(mode, n_embedded))
    print("   相对路径版 : {0} ({1:.1f} KB)".format(rel_out, os.path.getsize(rel_out) / 1024))
    print("   base64自包含: {0} ({1:.1f} KB)".format(b64_out, os.path.getsize(b64_out) / 1024))
    print("   下一步：Chrome/Edge 打开 -> 等图渲染 -> 复制 -> 粘到 mp.weixin.qq.com")


if __name__ == "__main__":
    main()
