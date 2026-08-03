# 高密度 storyboard.json 数据契约

在拆文章、生成线稿或调整动画时读取本文件。

## 拆镜与密度

- 每镜头只表达一个核心观点，旁白通常 1～2 句；优先使用 2～6 个镜头。
- 保留原文的因果顺序，不凭空增加事实、数字或结论。
- 每镜头默认设计 6～9 个语义模块、2～4 条箭头或关系线、3～5 个中文标注。
- `visualPrompt` 只描述可画出的对象和关系，明确要求白底、黑色手绘线条、无文字。
- 图片中的箭头和关系线作为独立模块或包含在相邻模块中，确保能按叙事顺序揭示。
- 同一条箭头不得被两个模块切开；箭身超出主体 `box` 时，把完整箭头范围加入该模块的 `extraRevealBoxes[]`。
- 构建器只在各模块边界框内显示底图；最后一个模块完成后才补齐完整底图，避免框外碎线提前泄漏。
- 每个模块通过独立透明裁切窗口揭示；未出场区域必须透明，禁止用白色遮罩覆盖其他模块，以免人物、箭头或物体在边界重叠处残缺。

## 顶层字段

- `version`：V2 固定为 `2`。
- `article`：标题、语言和文章路径。
- `contentProfile`：文章领域画像。包含 `domain`、`aiConfidence`、`resolvedDomainPreset`、`topics`、技术深度、受众、文章类型、识别信号和判断理由。
- `project.visualStyle`：固定为 `dense-whiteboard`，AI 文章也不得切换成科技 UI 或其他画风。
- `project.domainPreset`：默认 `auto`；也可显式使用 `general`、`hybrid` 或 `ai-explainer`。旧项目未填写时按 `general` 处理。
- `project.canvas`：画布尺寸与帧率。
- `project.transition`：当前固定为 `crossfade`。
- `project.timing`：旁白前导、结尾停留、揭示窗口和模块间隔。
- `project.captions`：字幕开关、最大组长度、底部安全区和样式。
- `narration`：默认 `macos-say`、`Tingting`、rate 241（旧版 rate 185 的约 1.3 倍）。
- `hand`：手部素材、显示尺寸、笔尖坐标和退场参数。
- `diagnostics.defaultEnabled`：调试为 `true`，正式输出必须为 `false`。
- `scenes`：按叙事顺序排列的镜头。

## 镜头字段

- `id`：以字母开头，只用字母、数字、下划线或连字符。
- `title`：项目识别名，不自动显示。
- `narration`：完整旁白。
- `captionChunks`：可选的人工字幕断句；每项是非空字符串。
- `visualPrompt`：无文字线稿提示词。
- `sourceImage`：项目内 16:9 底图路径。
- `visualPattern`：镜头的主结构，可用 `pipeline`、`architecture`、`comparison`、`loop`、`cause-effect`、`timeline`、`hub-spoke`、`metric-dashboard` 或 `general`。
- `aiConcepts[]`：AI 视觉词典概念与实际模块的绑定；每项包含 `key`、准确中文 `label` 和 `moduleId`。
- `modules`：依次揭示的语义区域。
- `annotations`：准确 HTML 中文知识标注。
- `techComponents`：可选的 HTML 技术组件，用于 Prompt、代码、API、指标、数据、风险、模型或工具名称。

## 模块字段

- `box.x/y/width/height`：模块在最终画布上的边界框。
- `role`：可选 `visual` 或 `card`。容器卡片使用 `card`；构建器会要求它至少关联一个框内标注，防止出现空白大框。
- `clipPolygon[]`：可选的精细静态裁切多边形，点坐标使用 0～1 的归一化值。用于人物与接触物合并后排除邻近箭头、石块或装饰线，渐进揭示发生在该多边形内部。
- `extraRevealBoxes[]`：可选的附加揭示框。用于跨出主体框的箭头、关系线或装饰笔画；这些区域与主 `box` 同时揭示，不增加新的时间步骤。
- `reveal.direction`：`down`、`up`、`right` 或 `left`。
- `reveal.edgePosition`：笔尖在边界上的相对位置，范围 0～1。
- `reveal.weight`：模块占揭示窗口的相对时长。

## 标注字段

- `id`：镜头内唯一标识。
- `text`：准确中文短语，通常 2～8 个字。
- `variant`：`title`、`label` 或 `callout`。
- `box`：标注容器位置；必须位于画布内且不得进入字幕安全区。
- `revealAfter`：关联模块 ID；该模块揭示完成后标注进入。
- `placement`：可选 `free` 或 `inside`。卡片内部小标题使用 `inside`，构建时会强制检查标注框完全位于关联模块主 `box` 内。
- `accentColor`：可选六位十六进制强调色。

## 技术组件字段

- `id`：镜头内唯一标识。
- `type`：`prompt-box`、`code-card`、`api-exchange`、`metric-badge`、`data-chip`、`risk-callout`、`model-badge` 或 `tool-badge`。
- `title`：准确技术标题；不得让线稿图片生成该文字。
- `body`：可选的简短说明。
- `lines[]`：可选的逐行代码、参数或请求内容；`code-card` 至少包含一行。
- `box`：组件位置，必须完全位于画布和字幕安全区之上。
- `revealAfter`：关联模块 ID；模块绘制完成后组件进入。
- `accentColor`：可选强调色；未填写时根据组件语义采用 AI 固定色义。

同一镜头内的技术组件不得互相重叠。正文较长时拆成新镜头，不缩小到无法阅读。

## 自动领域路由

`domainPreset: auto` 时必须填写 `contentProfile`，构建器按 `aiConfidence` 校验结果：

- 不低于 0.72：`ai-explainer`
- 0.45～0.72：`hybrid`
- 低于 0.45：`general`

识别方式和镜头模板见 `ai-scene-routing.md`；AI 概念映射见 `ai-visual-dictionary.md`。未知概念使用通用节点和准确 HTML 标签，不猜测图形。

## 字幕规则

- `project.captions.enabled` 为 `true` 时生成字幕。
- 优先采用 `captionChunks`；否则按标点自动拆成不超过 `maxChars` 的短组。
- 字幕时间按真实 WAV 时长和各组字符数分配，一次只显示一组。
- 每组退出后必须用确定性的 `tl.set` 隐藏，禁止残留到下一组。

## 自动时间

先生成 `assets/audio/<scene-id>.wav`，再构建。脚本用 `ffprobe` 读取真实长度并安排模块、标注、字幕和转场。没有有效 WAV 时只生成估算时间，并在输出中标记；估算不得作为正式成片依据。
