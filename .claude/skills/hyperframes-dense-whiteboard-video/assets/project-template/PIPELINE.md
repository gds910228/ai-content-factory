# 高密度文章白板视频流水线

输入为 `input/article.md`。Codex 先生成 `contentProfile`；画风固定为 `visualStyle: dense-whiteboard`，`domainPreset: auto` 只根据 AI 置信度解析为 `general`、`hybrid` 或 `ai-explainer`。随后生成 `storyboard.json`，逐镜头配置旁白、主视觉模板、无文字线稿、6～9 个揭示模块、3～5 个 HTML 中文标注、可选技术组件和字幕断句。

运行 `npm run make -- --output renders/article-final.mp4` 可依次生成或更新中文旁白、读取真实音频时长、生成组合、执行 HyperFrames 检查并渲染成片。

常用命令：

- `npm run voice`：按文本、voice 和 rate 缓存签名生成配音。
- `npm run build`：验证 storyboard 并生成组合与 manifest。
- `npm run check`：构建后执行 HyperFrames 检查。
- `npm run dev`：打开 Studio 预览。
- `npm run render -- --output renders/article-final.mp4`：渲染视频。

更换文章时只改 `input/article.md`、`storyboard.json` 和 `assets/scenes/`。AI 或混合文章按 Skill 的 AI 视觉词典填写 `visualPattern`、`aiConcepts` 和必要的 `techComponents`。`index.html`、`compositions/*.html` 与 `build-manifest.json` 都是生成文件，不要手改。
