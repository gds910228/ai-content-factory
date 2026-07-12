---
type: mixed
density: per-section
style: sketch-notes
palette: default (sketch-notes built-in macaron)
image_count: 5
aspect: "16:9"
language: zh
article: 02-稿件库/01-创作中稿件/我对Harness的观点和实操心得-20260712/05-发布包/长文发布包.md
backend: baoyu-image-gen (modelscope / Tongyi-MAI/Z-Image-Turbo, 2k)
watermark: false
---

# 配图大纲 - Harness不是越强越好

## Illustration 1

**Position**: 第一节末尾，"那一刻真的有点破防…想摔键盘"之后，"也正是这次翻车"之前
**Purpose**: 可视化裸用AI的级联崩溃循环（"打地鼠"的底层概念=失控循环，非直译比喻）
**Visual Content**: 圆形循环流程图：改A功能→B崩→修B→C崩→编译报错→循环；中心强调"改一个 崩一个"
**Type Application**: flowchart（circular loop），sketch-notes 手绘风
**Filename**: 01-flowchart-crash-loop.png

## Illustration 2

**Position**: 第三节，"整个过程，AI是干活的工人，我是拍板的老板…我审范围、定取舍"之后
**Purpose**: 可视化"用AI治AI"自定义搭建流程（真实落地步骤）
**Visual Content**: 左→右流程：读SOP→拉superpowers 14个skill→对照9项映射(5强/1自建/3砍)→落8skill+4Rules+Agent→通电CLAUDE.md
**Type Application**: flowchart（left-right），sketch-notes 手绘风
**Filename**: 02-flowchart-ai-builds-harness.png

## Illustration 3

**Position**: 第四节，配图位置标记处（"那种感觉怎么说呢…开跑车"之后的小技巧之后）
**Purpose**: 可视化搭Harness前后实测对比
**Visual Content**: 左右对比：左=搭建前(2~3轮扯皮/指令没执行/质量不过)，右=搭建后(一轮到位/拆得很细/细节拿捏)
**Type Application**: comparison（left-right split），sketch-notes 手绘风
**Filename**: 03-comparison-before-after.png

## Illustration 4

**Position**: 第五节，"实践出真知，这套判断我是自己一个个项目试出来的"之后
**Purpose**: 【核心反共识】可视化"该不该用Harness"判断标准：小项目别用 vs 大项目必须用 + 三条件
**Visual Content**: 左右对比：左=小项目·别用(三条件:代码量小/规范要求不高/不长远维护)，右=大项目·必须用(代码量大/长期迭代/规范高)
**Type Application**: comparison（left-right split），sketch-notes 手绘风，珊瑚红强调反共识
**Filename**: 04-comparison-small-vs-big.png

## Illustration 5

**Position**: 第六节，"Harness就这么越长越壮"之后
**Purpose**: 可视化活文档生长循环（踩坑→补规矩→不再犯→循环）
**Visual Content**: 圆形循环流程图：踩坑→补一条硬规矩→AI不再犯→新坑又来→循环；中心"越长越壮"
**Type Application**: flowchart（circular loop），sketch-notes 手绘风
**Filename**: 05-flowchart-living-doc-loop.png
