---
type: mixed
density: balanced
style: dark-tech
palette: default
language: zh
image_count: 5
article: 02-稿件库/01-创作中稿件/用了三个月AI，我反而看不懂自己的项目了-20260922/05-发布包/长文发布包.md
backend: baoyu-image-gen / modelscope / Tongyi-MAI/Z-Image-Turbo
insert_back: false
---

# 配图大纲：《用了三个月AI，我反而看不懂自己的项目了》

统一视觉基调（dark-tech）：深色代码编辑器质感（#0D1117 深炭底），荧光绿 #3FB950 为核心语义色（=「同意」按钮/AI 产出），红橙 #F85149/#FFA657 表警示/损失，蓝 #58A6FF / 紫 #BC8CFF 表代码/信息，浅灰 #E6EDF3 文字，等宽代码美学 + 柔和霓虹光晕。5 张图共用同一意象系统：发光绿色「同意」按钮。

## Illustration 0
**Position**: 封面（文章「封面图设计建议」节，公众号头条 900×383）
**Purpose**: 点击率锚点；「悬停未按的绿色同意按钮」是全文核心意象，三平台封面共用
**Visual Content**: 深色代码编辑器背景 + 发光绿色「同意」按钮 + 手指悬停未按；主标「别再无脑点同意了」大字居中，副标「3 道防线，把判断权拿回来」
**Filename**: 00-scene-cover-agree-button.png
**Aspect**: 21:9

## Illustration 1
**Position**: 开头钩子，段落「AI 甩出一个方案，你看一眼 diff，点个同意。一天几十次，次次如此。」之后、第一节标题之前
**Purpose**: 将「人退化成审批按钮」这一核心隐喻可视化，承接开头情绪
**Visual Content**: 巨大的发光绿色「同意」按钮上趴着渺小的开发者剪影，背景 diff 代码流快速滚过无人阅读，角落计数「今天 第 41 次同意」
**Filename**: 01-scene-mindless-approve.png
**Aspect**: 16:9

## Illustration 2
**Position**: 第一节末【配图1】占位处（5 信号自测清单之后）
**Purpose**: 收藏锚点，读者截图带走的核心资产（文章已规划）
**Visual Content**: 竖版自测卡：标题「5 个信号自测」+ 5 条信号勾选列表 + 底部红色结论条「中 3 条 = 审批按钮」
**Filename**: 02-infographic-5-signals-checklist.png
**Aspect**: 3:4

## Illustration 3
**Position**: 第二节，「点同意的成本是 3 秒，看懂的成本是 30 分钟……」段落之后
**Purpose**: 把「3 秒 vs 30 分钟」的算术题变成一眼可感的视觉对比，强化结构问题而非态度问题的论证
**Visual Content**: 左右对比：左侧「点同意 · 3 秒」（轻盈、绿色按钮、闪电），右侧「看懂 · 30 分钟」（沉重、代码文档堆、时钟）；底部警示条「任务全部成功，理解全部失败」
**Filename**: 03-comparison-3s-vs-30min.png
**Aspect**: 16:9

## Illustration 4
**Position**: 第四节防线三之后【配图2】占位处
**Purpose**: 全文方法论核心资产；三道防线流程图（文章已规划，900×600 横版）
**Visual Content**: 三阶段流程：事前（AI 出 2-3 方案 → 我选 + 一行决策）→ 事中（AI 讲一遍 → 我复述 ✓ 门禁）→ 事后（三行沉淀 → 回填新会话）；底部结论「+10 分钟，把判断权拿回来」
**Filename**: 04-flowchart-3-defense-lines-v4.png
**Aspect**: 3:2

---

## 定稿记录（视觉质检后）

| 序号 | 定稿文件 | 质检结论 | 弃用候选（保留备查） |
|---|---|---|---|
| 00 | 00-scene-cover-agree-button.png | ✅ 一次通过：标题/副标/按钮/手指全部正确 | — |
| 01 | 01-scene-mindless-approve.png | ✅ 一次通过：「同意」「今天第 41 次 · 同意」正确 | — |
| 02 | 02-infographic-5-signals-checklist-v3.png | ✅ 恰好 5 行、全空复选框、「审批按钮」正确、无版本角标 | v1（第4/5行重复缺字+误勾选）；v2（右上角泄漏 v2 角标） |
| 03 | 03-comparison-3s-vs-30min-v3.png | ✅ 左右对称标签「点同意/看懂」、无杂字、红条正确 | v1（「E6EDFO」杂字泄漏）；v2（右侧缺「看懂」标签） |
| 04 | 04-flowchart-3-defense-lines-v4.png | ✅ 全部文字正确 + 底部结论条 + 回环虚线箭头齐全（全图+局部放大双重核验） | v1（两处小字乱码）；v2（第三卡正文与底部条乱码）；v3（底部结论条缺失） |

生成引擎：ModelScope `Tongyi-MAI/Z-Image-Turbo`，经 baoyu-image-gen 批量接口，共 12 次生成（5 首轮 + 3 v2 + 3 v3 + 1 v4）。
