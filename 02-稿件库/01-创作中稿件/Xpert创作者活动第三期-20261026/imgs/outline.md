# outline.md — Xpert 第三期图卡系列（已定稿）

- strategy: A 故事驱动（续篇叙事：7个月 → 变化 → 日常 → 人群）
- style: notion（手绘线稿，延续上期已过审视觉体系）
- palette: 白底 + 淡彩蓝/黄/粉点缀
- backend: modelscope / Qwen/Qwen-Image / 2k
- 尺寸: 01-06 → 3:4（864×1152）· 07 → 9:16
- 生成日期: 2026-10-26

## 生成经验（Qwen-Image 中文文字卡）

- 数字"7"+个月混排标题乱码率高 → 改中文数字「第七个月」后稳定
- 文字元素 ≤3 组、每段 ≤10 字最稳；标签 2-4 字几乎不出错
- 常见泄漏（可容忍，先例：上期已发布卡同样有角落瑕疵）：角落伪logo/徽标、浏览器装饰条、小字乱码段
- 硬伤即弃：正文乱码、缺字、规格值入画（3:4/百分比/Type: Infographic）
- 胜选率约 1/4-1/5，多轮翻滚+择优是必要流程；落选稿存 `candidates/`

## 最终选定（提示词 → 成图）

| # | 成图 | 提示词 | 核对结果 |
|---|---|---|---|
| 01 | 01-xhs-cover-7months.png | prompts/01-cover-7months-v5.md | 标题2行+3标签+脚注全对 |
| 02 | 02-xhs-changes.png | prompts/02-list-changes-r2.md | 标题+3标签+脚注全对（节奏"变"快为通顺词） |
| 03 | 03-xhs-daily.png | prompts/03-balanced-daily-r5.md | 标题+3标签全对（左上角一枚乱码徽标，先例可容） |
| 04 | 04-xhs-fit.png | prompts/04-comparison-fit-r2.md | 标题+3标签+脚注全对（角落伪logo，先例可容） |
| 05 | 05-wx-cover-7months.png | prompts/05-wx-cover-r4.md | 标题2行+标签+Xpert脚注全对（装饰性浏览器涂鸦含Xpert，无碍） |
| 06 | 06-wx-daily.png | prompts/06-wx-daily-r3.md | 标题+3标签+脚注全对（顶部小"CRITICAL"泄漏，先例可容） |
| 07 | 07-video-cover.png | prompts/07-video-cover-r4.md | 大标题+副行+标签全对（顶部浏览器装饰条，先例可容） |

落选稿：`candidates/`（*-flawed-backup* / *-reject-b2 / *-r2 / *-r3 / *-r4）
