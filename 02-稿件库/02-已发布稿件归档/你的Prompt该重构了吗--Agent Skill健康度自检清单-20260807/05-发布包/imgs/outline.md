---
article: 02-稿件库/01-创作中稿件/你的Prompt该重构了吗--Agent Skill健康度自检清单-20260807/05-发布包/长文发布包.md
type: mixed
density: per-section
style: sketch-notes
palette: macaron
language: zh
image_count: 6
backend: baoyu-image-gen (modelscope / Z-Image-Turbo, quality=2k)
consolidation: "merged author 配图3(规则打架)+配图4(重复散落) -> single image 03; 正文 6->5; +封面 = 6 张"
---

# Illustration Outline — Prompt 健康度自检清单

## Illustration 1
**Position**: 开头金句后（"AI 连修 3 次都没修对…是我的 Prompt 病了"之后）
**Purpose**: 痛点共鸣——让读者一眼认出"连修3次都精确修错地方"的崩溃瞬间
**Visual Content**: 手绘开发者小人对着屏幕，三轮修改（第1/2/3轮）逐次排开，第三轮凭空冒出一个枚举值（珊瑚红高亮+?），气泡"精确地修错地方"
**Filename**: 01-infographic-triple-fix-fail.png
**Aspect**: 16:9

## Illustration 2
**Position**: 第1问金句后（"我自己都读不下去的，模型肯定也读不动"之后）
**Purpose**: 原理可视化——注意力 U 形曲线，走神位置 ≈ 模型丢东西位置
**Visual Content**: U 形曲线（开头高/中间低/结尾高），中间低谷标注"你走神 ≈ 模型丢东西"，标注"500行"长度阈值与"300-500行甜区"色带
**Filename**: 02-infographic-u-curve-attention.png
**Aspect**: 16:9

## Illustration 3
**Position**: 第4问金句后（合并原配图3+配图4；移除原配图3 callout）
**Purpose**: 冲突+重复可视化——规则失序的两种症状
**Visual Content**: 双区：左"互相打架"（规则A覆盖四维度 vs 规则B只展开异常，模型"合理地跳过"）；右"重复散落"（Ctrl+F 搜 严禁/必须/不得 散落，×3/×5/×8，"抢注意力"）
**Filename**: 03-infographic-rules-disorder.png
**Aspect**: 16:9

## Illustration 4
**Position**: 第6问末尾（"课本违反了规则，模型就会…反复横跳"之后）
**Purpose**: 一致性可视化——规则 vs 模板矛盾，模型在"听老师"与"照课本"间横跳
**Visual Content**: 左右对照：左规则"跳过某字段/四个维度不能漏"，右模板"SELECT 该字段/只覆盖两个维度"，中间模型图标在"听老师↔照课本"间反复横跳
**Filename**: 04-comparison-rule-vs-template.png
**Aspect**: 16:9

## Illustration 5
**Position**: 第7问后、第二节前（核心收藏资产，可截图）
**Purpose**: 核心收藏资产——可截图保存的 7 问自检清单卡片
**Visual Content**: 竖版卡片，第0问+①-⑦共8行，每行"问->开方"简写，底部"先号脉，再开方"+系列标识⑤
**Filename**: 05-infographic-checklist-card.png
**Aspect**: 3:4

## Illustration 6
**Position**: 文首/封面（头条封面，目标 900×383 ≈ 2.35:1，modelscope 用 21:9→1536×640）
**Purpose**: 系列头条封面——听诊器把脉厚 Prompt 文档，"病了?"反共识冲击
**Visual Content**: 厚文档堆（标注1500行）+ 听诊器把脉 + "病了?"问号；主标题"Prompt不是越加越稳"，副标题"别再加规则了，先给它把个脉"；左上系列标识⑤
**Filename**: 06-cover-prompt-pulse.png
**Aspect**: 21:9
