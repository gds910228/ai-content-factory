---
type: mixed
density: minimal-3
style: notion
palette: default
image_count: 3
article: 04-定稿.md
created: 2026-11-06
note: 文章已有5张真实截图（累计收入/众测任务记录/提示词迭代记录/质检流程/邀请码），本批3张为补充概念图；按作者要求不嵌回文章，仅存目录
---

# 插图大纲

> **生成结果（2026-11-06，modelscope / Qwen/Qwen-Image / 16:9 / 2k）**
> - 01 难度分规则卡：✅ 核验通过（无缺字/无色值入画；刻度尺端点 0/100 未标数字属轻微偏差可接受）
> - 02 四步流水线：✅ 主体文字全部正确、结构一致；角落有模型自行添加的杂字（左上 LayoutUI:02/Style:黑白、右上 Notion 标识），不影响主体信息，精修可选
> - 03 时薪三档：v1 ❌ 报废（色值入画+数字错+乱码）、v2 ❌ 报废（英文结构词被画入图）、**v3 ✅ 核验通过（全中文提示词方案）**
> - 废稿保留：03-infographic-hourly-rates.png、03-infographic-hourly-rates-v2.png（对比用，勿发布）
> - **最终可用图：01/02 原名 + 03 用 v3 文件**
> - 经验沉淀：Qwen-Image 会把提示词中的英文结构词（BAND/Data Visualization）渲染成可见文字，中文信息图提示词必须全中文、零英文 token

## Illustration 1
**Position**: 第三章「难度分规则」段后（……50分以下才算过关。）
**Purpose**: 难度分=模型得分率、越低越好，是全文最反直觉的规则，读者最容易看晕，需要一张科普卡把 90分❌/44分✅ 的反差画出来
**Visual Content**: 一条 0-100 的横向刻度尺，50 分处一条达标分界线；左区（<50）标"通过"配蓝色高亮和 ✓，右区（>50）标"太容易"配粉色和 ✗；刻度尺上方两个气泡示例：90分→打回，44.22→通过
**Filename**: 01-infographic-difficulty-score.png

## Illustration 2
**Position**: 第四章「四大步骤：首轮出题、加固返修、本地自测、自测后优化。」句后
**Purpose**: 四步流水线是全文方法论核心，现有截图只是文件列表，缺一张流程图让读者一眼看懂闭环
**Visual Content**: 左→右四个手绘圆角卡片（①首轮出题：难度埋在材料里 → ②加固返修：按分数分档 → ③本地自测：双窗口跑3次 → ④自测后优化：反向检查），④到②有一条返修循环虚线箭头，底部一句总结"难度来自材料，不来自题面"
**Filename**: 02-flowchart-four-step-pipeline.png

## Illustration 3
**Position**: 第六章「时薪」段后（……时薪大概150到360。）
**Purpose**: 三档时薪纯数字表达不直观，用横条对比图呈现"一次过 vs 返修一轮 vs 期望折算"的递减关系，呼应诚实账本主题
**Visual Content**: 三根横向手绘条形（一次通过 370-900 / 返修一轮 220-520 / 期望折算 150-360，单位：元/小时，挂机口径），条长按区间比例递减，右上角小注"质检不过不结算"
**Filename**: 03-infographic-hourly-rates-v3.png（终版；v1/v2 废稿保留对比）
