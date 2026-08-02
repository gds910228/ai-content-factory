# -*- coding: utf-8 -*-
"""
生成「公众号发布版」HTML —— 两种版本，一次产出。

为什么用脚本而不用 LLM 直接写 base64？
  4 张配图共约 2.8MB，base64 后近 4MB 纯文本，会让 LLM 输出 token 爆掉 (400)。
  所以 base64 编码这步交给本地脚本做，LLM 全程不碰图片二进制。

输入：长文发布包_排版_红白色系(red-white)_预览.html  (已有的带「复制到公众号」按钮的预览页)
输出：
  1) 长文发布包_公众号发布版.html         —— <img src="imgs/xx.png"> 相对路径版（推荐，体积小）
  2) 长文发布包_公众号发布版_自包含.html   —— base64 内嵌版（单文件可移植，体积大）

用法：python 生成公众号发布HTML.py
"""
import base64
import os
import sys

# Windows 控制台默认 GBK，打印 emoji 会崩；强制 stdout 用 utf-8 + 容错
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_HTML = os.path.join(HERE, "长文发布包_排版_红白色系(red-white)_预览.html")
IMGS = os.path.join(HERE, "imgs")

# 配图规格：(操作, 锚点文本, 图片文件名, alt, 图注)
#   操作 'replace' : 替换包含「锚点文本」的那个占位 <section>...</section>
#   操作 'insert'  : 在包含「锚点文本」的那个 <p>...</p> 之后插入图片
SPECS = [
    ("replace", "此处插入：恶性循环闭环流程图", "01-flowchart-vicious-loop.png",
     "恶性循环闭环流程图",
     "图1｜恶性循环闭环：越强调越长 → 越长越分散 → 越分散越违反 → 违反了再追加 → 绕回原点"),
    ("insert",  "我强调得越多，它崩得越准。", "02-comparison-99-vs-1.png",
     "99% 执行 vs 1% 崩塌 对照图",
     "图2｜99% 机械拆分乖乖执行 vs 1% SSE 时序崩了——瓷砖贴整齐了，承重墙拆错了"),
    ("replace", "此处插入：U 形注意力曲线示意图", "03-infographic-u-curve-attention.png",
     "U 形注意力曲线示意图",
     "图3｜注意力 U 形曲线：中间区域最易被遗忘（引自 Stanford《Lost in the Middle》）"),
    ("replace", "此处插入：4 个底层原因四宫格总结图", "04-framework-four-reasons.png",
     "4 个底层原因四宫格总结图",
     "图4｜越强调越崩的 4 个底层原因：U 形曲线 / 静默择一 / 粉红大象 / 上下文淘汰赛"),
]


def img_section(src, alt, caption):
    return (
        '    <section style="margin:8px 0 28px;text-align:center;">\n'
        '      <img src="{src}" alt="{alt}" '
        'style="max-width:100%;height:auto;display:block;margin:0 auto;'
        'border-radius:12px;border:1px solid #FEE2E2;'
        'box-shadow:0 6px 20px -8px rgba(220,38,38,0.22);" />\n'
        '      <p style="margin:10px 0 0;font-size:12px;color:#9CA3AF;'
        'line-height:1.6;letter-spacing:0.3px;">'
        '<span leaf="">📷 {cap}</span></p>\n'
        '    </section>'
    ).format(src=src, alt=alt, cap=caption)


def replace_placeholder(html, key, section_html):
    i = html.find(key)
    if i < 0:
        sys.exit("❌ 找不到占位文本: " + key)
    start = html.rfind("<section", 0, i)
    end = html.find("</section>", i)
    if start < 0 or end < 0:
        sys.exit("❌ 找不到占位 <section> 边界: " + key)
    end += len("</section>")
    return html[:start] + section_html + html[end:]


def insert_after_p(html, key, section_html):
    i = html.find(key)
    if i < 0:
        sys.exit("❌ 找不到插入锚点: " + key)
    end = html.find("</p>", i)
    if end < 0:
        sys.exit("❌ 找不到锚点 </p>: " + key)
    end += len("</p>")
    return html[:end] + "\n" + section_html + html[end:]


def build(html, src_for):
    for kind, key, fname, alt, cap in SPECS:
        sec = img_section(src_for(fname), alt, cap)
        if kind == "replace":
            html = replace_placeholder(html, key, sec)
        else:
            html = insert_after_p(html, key, sec)
    # 更新顶部提示条文案
    html = html.replace(
        "下方是排版效果 · 点右侧 <b>复制</b> 直接粘到公众号",
        "下方是含 4 张配图的终稿 · 点右侧 <b>复制</b> → 粘到公众号编辑器（图片会自动带入）",
    )
    return html


def main():
    # 前置检查
    if not os.path.isfile(SRC_HTML):
        sys.exit("❌ 找不到源文件: " + SRC_HTML)
    for _, _, fname, _, _ in SPECS:
        p = os.path.join(IMGS, fname)
        if not os.path.isfile(p):
            sys.exit("❌ 找不到配图: " + p)

    with open(SRC_HTML, "r", encoding="utf-8") as f:
        base = f.read()

    # 版本一：相对路径（推荐）
    rel = build(base, lambda fn: "imgs/" + fn)
    rel_out = os.path.join(HERE, "长文发布包_公众号发布版.html")
    with open(rel_out, "w", encoding="utf-8") as f:
        f.write(rel)

    # 版本二：base64 自包含（兜底）
    def data_uri(fn):
        with open(os.path.join(IMGS, fn), "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return "data:image/png;base64," + b64

    b64 = build(base, data_uri)
    b64_out = os.path.join(HERE, "长文发布包_公众号发布版_自包含.html")
    with open(b64_out, "w", encoding="utf-8") as f:
        f.write(b64)

    print("✅ 生成完成：")
    print("   相对路径版 :", rel_out, "(%.1f KB)" % (os.path.getsize(rel_out) / 1024))
    print("   base64自包含:", b64_out, "(%.1f KB)" % (os.path.getsize(b64_out) / 1024))


if __name__ == "__main__":
    main()
