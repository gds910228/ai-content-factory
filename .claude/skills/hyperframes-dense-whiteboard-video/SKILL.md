---
name: hyperframes-dense-whiteboard-video
description: "Turn an article, essay, notes, script, or storyboard into a high-density Chinese knowledge-explainer video in HyperFrames: automatically recognize AI explainers, route AI concepts to domain-specific visual patterns and HTML technical components, generate text-free whiteboard line art, add accurate labels and captions, reveal complete objects with a synchronized marker hand, create Chinese voiceovers, validate layouts, and render an MP4. Use for AI education, LLM/RAG/Agent/API explainers, dense knowledge diagrams, science or educational explainers, infographic-like whiteboard videos, captioned article-to-video automation, or a richer alternative to sparse whiteboard animation."
---

# HyperFrames 高密度知识白板视频

## 执行原则

把 Codex 作为编排层：拆文章、设计知识关系、生成无文字线稿、填写标注和字幕。把模板脚本作为确定性执行层：配音缓存、真实音频计时、透明裁切揭示、字幕切换、检查和渲染。

先读取并遵守可用的 HyperFrames、GSAP 和图像生成技能。不要修改简洁版 `hyperframes-whiteboard-video`；本 Skill 与其项目保持独立。

## 工作流

1. 运行 `python3 <skill-dir>/scripts/create_project.py <target-project-dir>` 创建独立项目。目标目录必须不存在或为空。
2. 把文章写入 `input/article.md`，读取 `references/storyboard.md`，先生成 `contentProfile`。保持 `project.visualStyle: dense-whiteboard`；`project.domainPreset` 默认使用 `auto`：AI 置信度不低于 0.72 时选 `ai-explainer`，0.45～0.72 时选 `hybrid`，其余回退 `general`。
3. 识别为 `ai-explainer` 或 `hybrid` 时，再读取 `references/ai-visual-dictionary.md`、`references/ai-scene-routing.md` 和 `references/ai-accuracy-rules.md`；通用文章不要加载或套用 AI 图形。
4. 将主线拆成 2～6 个镜头。每镜头只表达一个核心观点，但默认规划 6～9 个可揭示模块、2～4 条关系线和 3～5 个准确中文标注。不要添加文章没有支持的事实。
5. 为 AI 镜头填写 `visualPattern`、`aiConcepts` 和按需使用的 `techComponents`。只有需要准确代码、Prompt、API、指标或风险文字时才使用 HTML 技术组件。
6. 用图像生成能力逐镜头生成 16:9、白底、黑色线稿。图片必须无文字；标题、知识标签、技术文字和字幕全部通过 HTML 渲染。
7. 实际查看每张图并校准 `modules[].box`、`annotations[].box` 与 `techComponents[].box`。跨出主体框的完整箭头或连接线使用同一模块的 `extraRevealBoxes[]`，确保一次揭示；主体不得进入底部字幕安全区。
8. 运行 `npm run voice`。默认使用 macOS `Tingting`、rate 241（以旧版 rate 185 为基准的约 1.3 倍）；文本、voice 或 rate 改变时自动重新生成 WAV。
9. 运行 `npm run build`。脚本读取真实 WAV 时长，计算镜头、模块、标注、技术组件和字幕时间；未生成有效音频时只允许预览估算时间。
10. 开启 `diagnostics.defaultEnabled` 渲染草稿，检查裁切窗口、笔尖、标注框、技术组件和字幕安全区；正式输出时恢复为 `false`。
11. 运行 `npm run check`，再运行 `npm run render -- --output renders/final.mp4 --quality standard`。也可用 `npm run make -- --output renders/final.mp4` 串联整个流程。
12. 抽取英雄帧、字幕切换点和转场帧检查，并用 `ffprobe` 确认最终 MP4 的音视频流、尺寸和帧率。

## 画面约束

- 每镜头保留 110px 底部字幕安全区，主要图形占用上方约 70%～80% 画布。
- 使用 `Hannotate SC`，回退到 `Kaiti SC`、`PingFang SC`。标题 42～48px，知识标签 28～36px，字幕约 48px。
- 标注在关联模块揭示完成后进入并保持到转场；字幕一次只显示一组，结束时必须用 `tl.set` 强制隐藏。
- 一条语义完整的箭头必须归属于一个模块；不得让箭身和箭头分别由两个模块或最终底图补齐。
- 卡片、容器或面板的小标题必须放进对应框内，并设置 `placement: "inside"`；场景总标题和独立说明才允许使用框外位置。
- 不生成只有外框和角落图标的空卡片。卡片模块设置 `role: "card"`，并至少配置一个 `placement: "inside"` 的标题；没有原文支持的内容时应删除卡片，不得编造填充。
- 人物与其踩踏、持握或直接接触的物体若在扁平底图中互相重叠，应合并为一个揭示模块；使用 `clipPolygon` 精确排除邻近但不属于该组的图形。需要分时出现时，应改用独立透明素材，禁止用相互重叠的矩形裁切硬拆。
- 字幕优先使用 `captionChunks` 的人工断句；未提供时按中文标点和最多 16 字自动拆分。
- 保持纯白画布、黑色线稿，强调色只用于少量标签边框和重点。
- AI 模式遵守固定色义：青绿表示数据与检索，紫色表示模型与推理，橙黄表示成本或重点，红色仅表示风险与错误。
- AI 模式不得用机器人、大脑或芯片作为无意义装饰；每个 AI 图形必须映射到文案中的具体概念或关系。

## 验收标准

- 文章主线完整、镜头无明显重复、没有扩写未经支持的知识。
- 高密度镜头包含 6～9 个模块和 3～5 个准确中文标注；不足时构建器发出质量警告。
- AI 线稿没有乱码或伪中文，所有准确文字由 HTML 渲染。
- 首帧隐藏待揭示内容，模块依次出现，笔尖贴合裁切边界；每个物体使用独立透明裁切窗口，重叠模块不得用白色遮罩截断已出现的物体。
- 字幕不重叠、不越界、不遮挡主体，并在每组结束后完全隐藏。
- 镜头时长来自真实音频；相邻镜头使用交叉淡入，旁白不重叠。
- 正式画面关闭诊断层；HyperFrames 检查无错误和警告。
- `domainPreset: auto` 的解析结果必须与 `contentProfile.aiConfidence` 一致；`visualStyle` 始终为 `dense-whiteboard`。AI 镜头应使用明确的 `visualPattern`，未知概念回退通用节点而不是猜测错误图标。

## 失败处理

- 图像布局与提示词不一致时，以实际图片为准重新测量模块框，不猜测坐标。
- `say` 生成空音频时，用允许访问系统语音服务的权限重新运行，不把估算时长当正式配音。
- 标签侵入字幕区、越界或引用不存在模块时停止构建并修正 storyboard。
- HyperFrames CLI 不可用时，只交付项目文件并明确未完成的检查，不改用其他视频框架冒充完成。

## 资源

- `scripts/create_project.py`：从独立 V2 模板创建项目。
- `references/storyboard.md`：高密度拆镜规则和数据契约。
- `references/ai-visual-dictionary.md`：AI 概念到图形、关系和颜色的映射。
- `references/ai-scene-routing.md`：AI 文章识别、置信度和镜头模板路由。
- `references/ai-accuracy-rules.md`：AI 技术事实、品牌和时效性校验规则。
- `assets/project-template/`：字幕、标签、语音缓存、透明裁切、转场和渲染模板。
