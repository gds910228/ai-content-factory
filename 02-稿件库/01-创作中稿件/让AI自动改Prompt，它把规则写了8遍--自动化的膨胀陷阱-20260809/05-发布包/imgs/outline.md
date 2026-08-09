---
article: 02-稿件库/01-创作中稿件/让AI自动改Prompt，它把规则写了8遍--自动化的膨胀陷阱-20260809/05-发布包/长文发布包.md
type: mixed
density: per-section
style: sketch-notes
palette: macaron
language: zh
image_count: 5
backend: baoyu-image-gen (modelscope / Z-Image-Turbo, quality=2k)
series: "Prompt 工程系列 ④，视觉与①②③⑤统一（暖米纸+黑手绘线+马卡龙色块+单一珊瑚红强调）"
---

# Illustration Outline - 自动化的膨胀陷阱

## Illustration 1
**Position**: 开头破发后（"那一刻我是真有点破防…扫地机器人…垃圾倒堆成了一座小山"之后）
**Purpose**: 痛点共鸣--让读者一眼认出"改了四轮绕回原点、自动化勤勉却帮倒忙"的荒诞瞬间
**Visual Content**: 环形四阶段回路（一/二/三/四），每阶段提示词文档逐渐变厚，第四阶段一个回环箭头绕回第一阶段原点（珊瑚红强调）；环上一个勤恳小人图样不断往文档上加小色块。底部金句：自动化越勤勉，膨胀越静音
**Filename**: 01-infographic-loop-to-origin.png
**Aspect**: 16:9

## Illustration 2
**Position**: 第二章末（"每一步单看都合理，整体却是灾难…当前 LLM 就是结构性做不到全局扫描"之后）
**Purpose**: 机制可视化--单 badcase 决策树，AI 只走"追加"这条最安全路径
**Visual Content**: 双栏对照：左"现实路径"三步盒（读 badcase 描述 → 生成新规则 → 找位置插入，末尾标"追加"）；右"理想路径"四步盒（通读找已有 → 分析根因 → 最小化修改，末尾标"改"）。中间大叉，AI 路径标"只走最安全那条"（珊瑚红强调在"追加"）
**Filename**: 02-comparison-decision-tree.png
**Aspect**: 16:9

## Illustration 3
**Position**: 第三章末（"就像你雇了个特别勤快的小工…那堵墙本来就是你第一阶段就砌好的"之后）
**Purpose**: 量化可视化--四阶段膨胀曲线，行数一路上涨再绕回原点
**Visual Content**: 四阶段柱状/曲线（初版~百行 → +1轮失败 两三百行 → 又两轮 四五百行 → 绕回原点 又涨一截），柱高递增，第四阶段回环箭头绕回第一阶段；标注"同规则散布 8 处""膨胀 2.75 倍"（珊瑚红强调在"2.75倍"）。底部金句：每次一小段，累积好几倍
**Filename**: 03-infographic-bloat-curve.png
**Aspect**: 16:9

## Illustration 4
**Position**: 第四章金句后（"换个工具是治标，认清元凶、加上约束，才是治本"之后）
**Purpose**: 治疗认知可视化--换工具=治标 vs 认清元凶加约束=治本
**Visual Content**: 双栏对照：左"治标"（换更强模型 / 更聪明工具，打叉）；右"治本"（认清元凶 + 加约束：行数预算 / 语义去重 / 单次上限，打勾）。中间膨胀机器小图标。底部金句：执行交自动化，判断留给人（珊瑚红强调在"治本"打勾）
**Filename**: 04-comparison-treat-symptom.png
**Aspect**: 16:9

## Illustration 5
**Position**: 文首/封面（头条封面，目标 900×383 ≈ 2.35:1，modelscope 用 21:9）
**Purpose**: 系列头条封面--膨胀机器吞吐 + 绕回原点 + 反共识主标题
**Visual Content**: 左：一台"膨胀机器"，左边喂进一张清爽小 Prompt 文档，右边吐出一份臃肿绕圈的巨长文档，文档上一个回环箭头绕回起点，旁浮珊瑚红"？"。右：大号手写主标题"你把 Prompt 维护外包给 AI"，下方副标题"等于亲手养了台膨胀机器"。左上角圆角徽章"Prompt 工程系列 ④"
**Filename**: 05-cover-bloat-machine.png
**Aspect**: 21:9
