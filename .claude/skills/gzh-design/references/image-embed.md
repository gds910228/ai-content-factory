# 本地配图带入公众号（image-embed）

> 主流程（SKILL.md 工作流）假设图片是**公网 URL**：`![说明](https://...)` -> 2a 图片组件 `<img src="URL">`，粘贴时公众号直链抓取并转存。
> 但当**图片是本地文件**（`imgs/01.png`、截图、本地生图），公网 URL 没有，主流程带不过去。本文件讲这种情况。
> 按需加载：只有图片是本地文件、或遇到「LLM 写 base64 爆 token/400」时才读本文件。

## 一、铁律：绝不让 LLM 在 HTML 里手写 base64

N 张图（常 2~4MB）转 base64 是数 MB 纯文本，会让 LLM 输出 token 爆掉、API 返回 **400**、整段会话崩溃无法继续。

**所有 base64 编码移出 LLM 上下文**，二选一：
- **浏览器**：复制瞬间把渲染好的 `<img>` 序列化进剪贴板（相对/file 路径自动转 data-URI）；或
- **本地脚本** `scripts/build_gzh_html.py`：读图转 base64 注入 HTML，本地跑无上下文限制。

LLM 全程只写 `<img src="imgs/x.png">` 这种短标签。

## 二、为什么"浏览器复制"能把本地图带入公众号

在浏览器里对含 `<img>` 的选区执行复制（按钮 `document.execCommand('copy')` 或手动 Ctrl/⌘+A->C），浏览器往剪贴板写 `text/html`，**图片 src 被改写成 data-URI**（即使是 `imgs/x.png` 相对路径或 `file://`）。公众号编辑器粘贴时识别 `<img src="data:...">`，上传到自己的图床，再把 src 换成公众号地址。

**推论**：只要图在浏览器里渲染出来了，复制就带得过去——与 src 是相对路径还是 data-URI 无关。所以相对路径版（小）就够用；base64 自包含版只是"图肯定渲染 + 单文件可移植"的保险。

公众号**封外部图床热链**，本地图只能走"剪贴板粘贴"或其自带素材库，不能靠外部 URL。

## 三、工作流

主流程产出 `_预览.html` 后（图片处是 2c 占位框，或已是 `<img src="imgs/x.png">` 相对路径），跑一次脚本产出两个版本：

```bash
<SKILL_ROOT>/scripts/build_gzh_html.py \
  --src "<...>_预览.html" \
  --imgs "<imgs目录>" \
  [--spec "<spec.json>"]
```

- `--spec`（可选）：预览里是 2c 占位框时，声明每张图放哪，脚本按 2a 图片组件注入。
- 不传 `--spec`：只把已有的 `<img src="imgs/...">` 转成 base64 自包含版。

| 产物 | 体积 | 图片 | 用途 |
|---|---|---|---|
| `_含图.html` | 小 | `imgs/x.png` 相对路径 | **首选**。须与 `imgs/` 同目录。 |
| `_含图_自包含.html` | 数 MB | base64 内嵌 | 兜底 / 单文件移植。 |

然后：Chrome/Edge 打开（Obsidian 不渲染网页，须真浏览器）-> 等图渲染 -> 点「复制到公众号」或手动 Ctrl/⌘+A->C（图多时手动更稳）-> mp.weixin.qq.com 编辑器 Ctrl/⌘+V。图随样式带入并自动转存。

## 四、spec.json 格式（仅占位框模式需要）

```json
[
  {"op":"replace","anchor":"占位框里唯一文本","file":"01.png","alt":"图说","caption":"图1｜..."},
  {"op":"insert", "anchor":"某段落里唯一一句","file":"02.png","alt":"图说","caption":"图2｜..."}
]
```

- `op=replace`：替换包含 `anchor` 文本的整个 `<section>...</section>`（2c 占位框）。
- `op=insert`：在包含 `anchor` 文本的 `</p>` 之后插入图（无需占位框）。
- `anchor` 必须在源 HTML 中唯一、只出现一次。`caption` 可空（空则不加说明 `<p>`，符合"不硬造说明"）。

注入的图片用通用库 2a 标准图片组件（白底卡片 + 居中 `<img max-width:100%>` + 可选说明），`<span leaf="">` 包裹，过 `validate_gzh_html.py`。

## 五、排错（按优先级）

1. 改手动全选 + 复制（不用按钮）。
2. 换浏览器 Chrome ↔ Edge。
3. 改用 `_含图_自包含.html`。
4. 确认图在浏览器里真渲染出来了（没渲染就复制，剪贴板里没图）。
5. 兜底：先粘正文，再逐张用公众号「图片」按钮上传到对应位置。

## 六、顺序提醒

先对**干净正文**跑 `validate_gzh_html.py` 过校验 -> `wrap_preview.py` 出预览 -> 再跑 `build_gzh_html.py` 嵌图。嵌图产物是预览页（含按钮/脚本），不必再过校验（校验只针对干净 section）。
