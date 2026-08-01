---
type: mixed
density: balanced
style: sketch-notes
palette: macaron
image_count: 4
backend: baoyu-image-gen
provider: modelscope
model: Tongyi-MAI/Z-Image-Turbo
quality: 2k
aspect_ratio: "16:9"
language: zh
source_article: 02-稿件库/01-创作中稿件/你越强调AI越不听话--Prompt工程里的恶性循环-20260730/05-发布包/长文发布包.md
---

# 配图大纲｜AI不是越强调越听话

> 风格：sketch-notes（暖奶油纸 #F5F0E8 + 黑色手绘线 #1A1A1A + macaron 粉彩块）
> 配色上限：每图最多 4 种粉彩块色，黑色负责所有线条/文字，珊瑚红 #E8655A 仅作 1-2 处强调
> 类型兼容：infographic / framework / flowchart / comparison 均为 sketch-notes ✓✓ 最佳匹配

---

## Illustration 1

**Position**: 第二章末尾，"一个完美的恶性循环，闭环了。"之后
**Purpose**: 把"越强调越长"的恶性循环物证可视化，强化"第四阶段≈第一阶段、绕回原点"的冲击力
**Visual Content**: 圆形闭环流程图，4 个节点环形排列：①越强调越长 ②越长越分散 ③越分散越违反 ④违反了再追加，箭头回到起点；圆心标注"第四阶段 ≈ 第一阶段（绕回原点）"
**Type Application**: flowchart（circular layout）- sketch-notes 手绘圆角卡片 + 波浪箭头
**Filename**: 01-flowchart-vicious-loop.png

## Illustration 2

**Position**: 第三章末尾，"SSE 不是被 AI 弄崩的，是被我那份膨胀的"铁律"喂崩的。"之后
**Purpose**: 可视化"99% 乖乖执行 vs 最后 1% SSE 崩了"的破防反差
**Visual Content**: 左右对照。左侧大块薄荷绿区"99% 机械拆分乖乖执行"（分层/分批/零变更，整齐瓷砖图标+✓）；右侧小块珊瑚红区"1% SSE 时序崩了"（started/heartbeat/stream-fallback，拆错承重墙图标+✗）；底部小字"瓷砖贴整齐了，承重墙拆错了"
**Type Application**: comparison（left-right split）- sketch-notes 两块粉彩对照 + 手绘分隔线
**Filename**: 02-comparison-99-vs-1.png

## Illustration 3

**Position**: 第四章第 1 点（U 形曲线段），"那个被跳过的鉴权字段，就是因为它被埋在了中间偏后的位置。"之后
**Purpose**: 用一张图讲清"位置决定优先级，不是规则重要不重要决定优先级"
**Visual Content**: U 形注意力曲线。横轴=Prompt 位置（开头→中间→末尾），纵轴=模型注意力；两端高、中间低谷标注"遗忘区"；中间低谷处用珊瑚红标记"鉴权字段埋点"；引用论文标题《Lost in the Middle》
**Type Application**: infographic - sketch-notes 手绘坐标系 + U 形曲线
**Filename**: 03-infographic-u-curve-attention.png

## Illustration 4

**Position**: 第四章末尾（第 4 点之后、"## 五"之前），作为 4 个底层原因总结
**Purpose**: 把 4 个底层原因沉淀成"能截图带走的判断标准"，提升收藏率
**Visual Content**: 2×2 四宫格。①U 形曲线-中间最易遗忘 ②静默择一-不报错偷偷选一条 ③粉红大象-越禁止越惦记 ④上下文淘汰赛-多轮被挤没；每格一个粉彩色块+简笔图标+一句关键词；底部 takeaway"问题不在 AI 能力，在你把强调当万能解药"
**Type Application**: framework（2×2 matrix）- sketch-notes 四宫格 + 手绘连接
**Filename**: 04-framework-four-reasons.png
