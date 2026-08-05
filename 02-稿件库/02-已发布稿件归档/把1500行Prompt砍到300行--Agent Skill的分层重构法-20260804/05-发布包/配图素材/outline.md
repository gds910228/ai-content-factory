---
type: mixed
density: balanced
style: sketch-notes
palette: macaron
image_count: 4
backend: baoyu-image-gen (provider=modelscope, model=Tongyi-MAI/Z-Image-Turbo, quality=2k, ar=16:9)
output_dir: 配图素材/
language: zh
article: 02-稿件库/01-创作中稿件/把1500行Prompt砍到300行--Agent Skill的分层重构法-20260804/05-发布包/长文发布包.md
note: |
  上一会话爆 400 的根因：让 LLM 输出 4MB base64 文本撑爆输出 token。
  本次修复：编码/存盘交给 baoyu-image-gen 的 modelscope provider（脚本直接把
  返回的图片 URL 下载为二进制写盘），LLM 只写 markdown 图片链接，不碰 base64。
---

# 配图规划 · 把 1500 行 Prompt 砍到 300 行（Agent Skill 分层重构法）

全文约 3200 字，5 章。按文章自带「配图建议」配 4 张，统一 sketch-notes 手绘笔记风
格 + macaron 柔和色块，16:9。

## Illustration 1

**Position**: 第一章末尾（"得把这俩大文件拆开、分层重排"之后，配图1引文处）
**Purpose**: 把"几千行读不动、排查崩溃"的痛点具象化，引发共鸣
**Visual Content**: 一个人对满屏几千行代码 Ctrl+F 来回跳、满头大汗；旁边 AI 气泡写"要吞整份文件才看得懂"
**Type Application**: scene（sketch-notes 渲染为简笔画场景：人物用简笔，代码屏 + AI 气泡为图示，非写实）
**Filename**: 01-scene-code-overload.png

## Illustration 2

**Position**: 第二章末尾（"是一个毛病"之后，配图2引文处）
**Purpose**: 可视化"代码 → Prompt"的逻辑转折，点明主线（提示词自己也膨胀、绕回原点）
**Visual Content**: 大代码文件 → 让 AI 评估 → 产出开发提示词 → 提示词也膨胀（绕回原点的循环箭头）→ 也得分层重构
**Type Application**: flowchart（手绘圆角步骤卡 + 粗手绘箭头 + 顶部绕回循环箭头）
**Filename**: 02-flowchart-prompt-bloat.png

## Illustration 3

**Position**: 第四章第 1 点（四层架构处，配图3引文处）
**Purpose**: 把"位置即优先级"核心机制一张图讲清，全文最该截图带走的图
**Visual Content**: 左侧从上到下四个色块（全局禁令·首因效应区 / 核心方法论 / 执行流程·允许遗漏 / 输出模板·近因效应区），右侧 U 形注意力曲线对齐首尾高峰
**Type Application**: framework（层级堆叠 + 右侧 U 形曲线标注首因/近因效应区）
**Filename**: 03-framework-four-layer.png

## Illustration 4

**Position**: 第四章第 5 点（表格优于散文处，配图4引文处）
**Purpose**: 用最直观的对比证明"结构化格式"的威力
**Visual Content**: 左侧一坨"如果…就…"散文（灰暗），右侧一张干净的两列表格（明亮），中间向上箭头标"遵循率↑"
**Type Application**: comparison（左珊瑚红/右薄荷绿分屏 + 中间向上箭头桥接）
**Filename**: 04-comparison-prose-vs-table.png
