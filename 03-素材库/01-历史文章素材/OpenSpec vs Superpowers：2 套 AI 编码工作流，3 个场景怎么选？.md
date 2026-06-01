---
title: "OpenSpec vs Superpowers：2 套 AI 编码工作流，3 个场景怎么选？"
source: "https://mp.weixin.qq.com/s/XZjUCxvpOmqOzWF6LrtFPA"
author:
  - "[[运维有术]]"
published:
created: 2026-06-01
description:
tags:
  - "clippings"
---
运维有术 *2026年3月31日 09:00*

> 🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 *68* 篇，AI 编程最佳实战「2026」系列第 *11* 篇
> 
> 大家好，欢迎来到 **术哥无界 | ShugeX ｜ 运维有术** 。
> 
> 我是 **术哥** ，一名专注于 AI 编程、AI 智能体、Agent Skills、MCP、云原生、AIOps、Milvus 向量数据库的 **技术实践者与开源布道者** ！

> **Talk is cheap, let's explore。无界探索，有术而行。**

![封面图](https://mmbiz.qpic.cn/sz_mmbiz_png/icibtH5FrDwPcicVYaZg52qoh51kzx2muGCdpGG3tcVHxcFSvY5zZTrX4rVAXK9D8jsd4fcLJ7EE7aiaa5HYKuYEEn1iasAs5tzPTqI5ylzmomXY/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

封面图

*图 1：OpenSpec vs Superpowers 信息图封面*

用 AI 编码工具做项目，你大概率踩过这样的坑：让 Claude Code 帮你重构一个模块，它改着改着就忘了之前定的方案；或者让 Cursor 写个新功能，它一顿操作猛如虎，结果测试全挂。

问题不在 AI 本身，在于 **缺少一套规范的工作流来约束它** 。

目前社区里有两套方案热度很高：Superpowers，GitHub 上 125K Star，中文社区已经有 7 篇以上的详细教程；OpenSpec，npm 包 `@fission-ai/openspec` v1.2.0，虽然公开讨论还不多，但源码架构设计相当精良。

一个管 **行为纪律** ，一个管 **规格管理** 。很多开发者以为二选一就行，实际上它们解决的是不同层面的问题。今天把两个工具的机制拆开讲清楚，再用三个真实场景告诉你怎么选。

## 1\. OpenSpec：给 AI 编码加上「规格说明书」

### 它到底是什么

OpenSpec 是 Fission AI 创建的 AI 原生规范驱动开发框架。一句话概括： **它让 AI 编码工具按照一份结构化的规格文档来干活，而不是随心所欲地写代码** 。

这个思路的出发点很实际。AI 编码工具写代码很快，但写出来的东西经常偏离需求。你让它改个登录逻辑，它顺手把注册流程也改了。OpenSpec 的做法是：先把需求写成规格，再让 AI 按规格执行。

### 增量规格系统：不重写，只追加

这是 OpenSpec 的核心创新。

传统的规格文档有个致命问题：每次需求变更，要么重写整个文档，要么在旁边手动批注。OpenSpec 用了一个叫 **Delta-Based Specs** （增量规格）的机制，变更以增量形式表达：

- **ADDED Requirements** - 新行为追加到主规格
- **MODIFIED Requirements** - 替换现有需求块
- **REMOVED Requirements** - 删除需求块
- **RENAMED Requirements** - 用 `FROM:/TO:` 格式改标题

这个设计对 **棕地项目** （已有代码库的项目）特别友好。你不需要一次性把所有需求写全，发现遗漏了就直接追加一个 ADDED，发现某条描述不准确就 MODIFIED 替换。

```
# 增量规格示例
change:user-auth-refactor
deltas:
-type:ADDED
    title:"OAuth2 回调处理"
    requirement:|
      系统 SHALL 支持 Google OAuth2 回调，
      并在回调后自动创建或关联本地用户账户

-type:MODIFIED
    title:"密码重置流程"
    replaces:"密码找回"
    requirement: |
      密码重置 SHALL 通过邮件发送一次性链接，
      链接有效期 15 分钟
```

### DAG 工件依赖图：自动排执行顺序

OpenSpec 内部用了一个 DAG（有向无环图）来管理工作流的依赖关系，排序算法是 Kahn 算法的拓扑排序。默认的依赖关系长这样：

```
proposal（根节点）
    ├── specs（依赖：proposal）
    ├── design（依赖：proposal）
    │     └── tasks（依赖：specs, design）
    │           └── apply phase（依赖：tasks）
```

翻译成人话：你得先有提案（proposal），才能写规格（specs）和设计（design）；规格和设计都完成后，才能拆任务（tasks）；任务拆完了才能动手实现（apply）。

这个依赖关系不是写死的。OpenSpec 支持三层 Schema 自定义：

1. **项目本地** ： `<project>/openspec/schemas/<name>/schema.yaml`
2. **包内置** ： `<package>/schemas/<name>/schema.yaml`

### 验证引擎：写错规格能自动发现

OpenSpec 内置了一个验证引擎，会检查规格的完整性和一致性：

- **重复检测** ：发现内容重复的需求
- **跨节冲突检测** ：不同章节之间互相矛盾的地方
- **SHALL/MUST 关键字检查** ：确保需求用了 RFC 2119 标准的关键字
- **场景覆盖检查** ：需求有没有覆盖所有使用场景

### Agent 友好的 CLI 设计

OpenSpec 的 CLI 专门为 AI Agent 设计了 JSON 输出模式。AI 工具不需要解析人类可读的文本，直接拿到结构化数据：

```
# 获取当前变更状态
openspec status --change <name> --json

# 获取指定工件的指令
openspec instructions <artifact> --change <name> --json

# 获取可用模板
openspec templates --json
```

目前支持 22 个 AI 编码工具，包括 Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、RooCode、Cline、Kilo Code、Kiro、Trae 等。每个工具有专门的适配器，覆盖面是同类工具里比较广的。

### OpenSpec 的短板

公平起见，也得说说不方便的地方：

- 需要 Node.js >= 20.19.0，版本要求不低
- 目前只有 1 个内置 Schema（spec-driven），扩展需要自己写
- 没有内置实现验证 - 规格写好了，代码对不对还得靠测试
- 只支持 Markdown 格式
- 没有并行变更的冲突解决机制
- 没有 Web UI，纯命令行操作
![OpenSpec 架构图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

OpenSpec 架构图

*图 2：OpenSpec 架构图 - DAG 工件依赖关系与增量规格系统*

## 2\. Superpowers：给 AI 编码加上「行为纪律」

### 一套纯 Markdown 的行为约束系统

Superpowers（v5.0.6）是 Jesse Vincent（Prime Radiant）创建的，整个系统的本质是 **纯 Markdown + YAML 文档，作为 prompt 上下文注入 AI Agent 的对话** 。零运行时依赖，没有一行可执行代码。

这听起来有点反直觉 - 一个 125K Star 的项目，居然没有任何代码？

它的逻辑是这样的：AI 编码工具本身就有写代码的能力，问题不在于它 **能不能写** ，而在于它 **怎么写** 。Superpowers 做的事情是制定一整套行为规范，让 AI 按照 TDD（测试驱动开发）、系统化调试、代码审查等最佳实践来工作。

### 14 个技能组成的工作流管道

Superpowers 把开发流程拆成了 14 个技能（Skill），每个技能是一组 Markdown 文档，描述了在什么情况下触发、怎么执行、有哪些铁律：

| 技能 | 作用 |
| --- | --- |
| using-superpowers | 启动技能，每次响应前检查适用技能 |
| brainstorming | Socratic 设计，通过提问驱动方案形成 |
| using-git-worktrees | 创建隔离的 git worktree 做变更 |
| writing-plans | 把规格拆成 2-5 分钟的小任务 |
| subagent-driven-development | 每个任务派遣独立子 Agent + 两阶段审查 |
| test-driven-development | 严格 RED-GREEN-REFACTOR 循环 |
| systematic-debugging | 4 阶段根因调查 |
| verification-before-completion | 声明成功前必须提供证据 |
| requesting/receiving-code-review | 代码审查工作流 |
| finishing-a-development-branch | 合并/PR/清理 |
| dispatching-parallel-agents | 并行 Agent 派遣 |

其中最有意思的是 **subagent-driven-development** （子 Agent 驱动开发）。它的工作方式是：每个任务派遣一个拥有 **新鲜上下文** 的独立子 Agent 去完成，完成后经过两阶段审查 - 先查规格合规性，再查代码质量。子 Agent 结束时必须给出明确状态： `DONE` 、 `DONE_WITH_CONCERNS` 、 `BLOCKED` 或 `NEEDS_CONTEXT` 。

### 反合理化设计：专治 AI 的偷懒倾向

Superpowers 的设计里有一个很独特的思路： **反合理化（Anti-Rationalization）** 。

AI 编码工具有个通病 - 你让它严格按 TDD 来，它会说"好的"，然后该跳过测试的时候还是会跳过，还会给出看似合理的借口。Superpowers 的做法是在每个技能文档里列出常见的合理化借口和对应的反驳：

> 借口：这个功能太简单了，不需要测试。 反驳：简单功能出 bug 的概率并不低，而且测试本身就是文档。

这种设计不是拍脑袋想出来的。根据 Meincke et al.（2025）的研究，Superpowers 基于 Cialdini 的说服原则设计，在 N=28,000 次 AI 对话中验证，合规率从 33% 提升到了 72%。

### 5 个平台支持

Superpowers 目前支持 5 个平台：Claude Code、Cursor、Codex、OpenCode、Gemini CLI。比 OpenSpec 的 22 个少不少，但覆盖了主流工具。

说实话，Superpowers 在 Claude Code 上表现最好，其他平台有些功能（比如子 Agent 派遣）会受限于平台本身的能力。

### Superpowers 的短板

- **无实际代码执行** - 纯 prompt 工程，不能帮你跑测试或者检查构建
- **Token 消耗较大** - 14 个技能文档全部注入上下文，token 开销不小
- **过于有主见** - 严格的 TDD 流程对快速原型开发来说可能太重
- **无程序化强制执行** - 说到底还是靠说服 AI，不是硬约束
- **子 Agent 功能依赖平台支持** - 不是所有 AI 工具都支持派遣子 Agent
![Superpowers 技能管道流程图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Superpowers 技能管道流程图

*图 3：Superpowers 14 个技能的工作流管道*

## 3\. 三种场景，三套方案

前面拆了机制，现在落到具体场景。三种典型的开发场景，看看哪个工具更合适。

### 场景 A：大型企业项目的需求变更管理

**背景** ：一个运行了 3 年的 Java 微服务项目，50+ 模块，团队 8 个人。产品经理每周提 3-5 个需求变更，每个变更影响 3-8 个模块。

**核心痛点** ：需求变更频繁，变更之间容易冲突；AI 编码工具改着改着就偏离了原始需求；新来的团队成员对项目上下文不熟悉，AI 也不熟悉。

**推荐方案：OpenSpec**

理由很直接：

1. **增量规格系统正好对付频繁变更** 。每个需求变更写一个 delta，不需要每次重写整个规格文档。 `ADDED` 追加新行为， `MODIFIED` 替换旧描述，审计起来也方便。
2. **DAG 依赖图保证执行顺序** 。50+ 模块的项目，改动之间有前后依赖。OpenSpec 的拓扑排序能自动算出哪个任务先做、哪个后做。
3. **验证引擎防止需求冲突** 。两个需求改了同一个模块的不同行为，验证引擎能检测到跨节冲突，避免改出问题。
4. **22 个 AI 工具适配** 。团队里有人用 Cursor，有人用 Claude Code，有人用 Copilot，OpenSpec 都能接。

Superpowers 在这个场景下不太合适。它的强项是行为约束，但大型项目的核心挑战是 **规格管理** - 怎么把复杂的需求变更用结构化的方式管理起来。光有行为纪律，没有清晰的规格，AI 再守规矩也干不对活。

### 场景 B：个人开发者的快速原型迭代

**背景** ：独立开发者，一个人做一个 SaaS 产品，用 Claude Code 做主力编码工具。需求每天都在变，有时候上午的想法下午就推翻了。

**核心痛点** ：AI 编码工具经常跳过测试直接写实现；写出来的代码缺乏系统设计；调试时没有方法论，东改一下西改一下。

**推荐方案：Superpowers**

理由：

1. **零配置开箱即用** 。不需要写规格文档，不需要搭建工具链，把技能文档往 Claude Code 的上下文一塞就行。对于一个人快速迭代来说，写规格文档的时间成本太高。
2. **TDD 自动化** 。Superpowers 会强制 AI 先写测试再写实现。独立开发者最大的坑就是"先跑起来再说"，结果就是一堆没测试的代码。Superpowers 的反合理化设计能治这个毛病。
3. **系统化调试** 。4 阶段根因调查方法，比瞎猜效率高得多。
4. **验证前置** 。声明成功前必须提供证据，不能 AI 说"搞定了"就真搞定了。

OpenSpec 在这个场景下太重了。个人项目的需求变化太快，写规格文档的成本和收益不成正比。而且 OpenSpec 需要 Node.js >= 20.19.0，独立开发者的本地环境不一定满足。

### 场景 C：团队协作的规范化开发流程

**背景** ：一个 5 人团队开发一个中型 Web 应用，2 个后端、2 个前端、1 个全栈。用 Claude Code 和 Cursor 混合。项目从 0 开始，有比较明确的产品需求文档。

**核心痛点** ：多人同时开发，代码风格不统一；需求文档和实际实现脱节；AI 辅助编码的质量参差不齐，有人写出来的代码质量高，有人写出来的像屎山。

**推荐方案：OpenSpec + Superpowers 组合**

这个场景下，两个工具各管各的层面，互相补充：

**OpenSpec 管规格层** ：

- 把产品需求文档转成 OpenSpec 的规格文档，作为团队共享的 **单一信息源**
- 用 DAG 依赖图拆分任务，分配给不同团队成员
- 用验证引擎确保每个需求的实现都覆盖了所有场景
- 用增量规格系统管理需求变更，每次变更都有审计追踪

**Superpowers 管行为层** ：

- 所有团队成员的 AI 编码工具统一加载 Superpowers 技能文档
- 用 TDD 技能确保所有代码都有测试覆盖
- 用代码审查技能统一团队的代码质量标准
- 用子 Agent 驱动开发处理复杂任务，减少上下文污染

你在团队协作中用过类似的工作流方案吗？哪种组合方式更适合你的场景？欢迎在评论区聊聊。

![选型决策树](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

选型决策树

*图 4：三种场景选型决策树*

## 4\. OpenSpec + Superpowers 组合实战方案

两个工具怎么组合？说一个具体的操作思路。

### 第一层：用 OpenSpec 做项目骨架

```
# 安装 OpenSpec
npm install -g @fission-ai/openspec

# 初始化项目
openspec init

# 创建提案
openspec propose "用户认证模块重构"

# 编写规格（AI Agent 会自动读取并按规格执行）
openspec spec --change user-auth-refactor
```

项目初始化完成后，OpenSpec 会在项目根目录生成 `openspec/` 目录，里面包含提案、规格、设计和任务文件。这些文件就是团队共享的 **规格基准** 。

### 第二层：用 Superpowers 做行为约束

把 Superpowers 的技能文档放在项目的 `.claude/` 目录（Claude Code）或者 `.cursor/` 目录（Cursor），作为 AI 编码工具的上下文注入。

关键是只选需要的技能，不要全量加载。对于一个中型 Web 项目，推荐的技能组合是：

- **test-driven-development** - 所有开发任务必选
- **writing-plans** - 任务拆分
- **systematic-debugging** - 调试场景
- **verification-before-completion** - 验证收尾
- **requesting-code-review** - 代码审查

5 个技能的 token 开销比全量 14 个小很多，同时覆盖了开发流程的关键环节。

### 第三层：让两者协作

```
OpenSpec 规格文档 → 作为 Superpowers writing-plans 技能的输入
     ↓
Superpowers 拆分任务 → 每个任务对照 OpenSpec 规格执行
     ↓
Superpowers TDD 技能 → 按规格写测试，再写实现
     ↓
OpenSpec 验证引擎 → 检查实现是否满足规格
     ↓
Superpowers 验证技能 → 提供测试通过的证据
```

这个流程的核心思路是：OpenSpec 定义"做什么"，Superpowers 定义"怎么做"。

### 组合方案的注意事项

说实话，这套组合方案也有坑：

1. **Token 消耗叠加** 。OpenSpec 的规格文档加上 Superpowers 的 5 个技能文档，注入 AI 上下文的 token 量不小。Claude Code 的上下文窗口一般够用，但 Cursor 和 Copilot 可能会觉得挤。
2. **维护成本** 。两套工具都要维护配置。OpenSpec 的规格文档需要持续更新，Superpowers 的技能选择需要根据项目阶段调整。
3. **学习曲线** 。团队成员需要同时理解两套工具的运作逻辑。如果团队里有人连 Git 都不太熟，上这套方案可能会适得其反。
![组合方案架构图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

组合方案架构图

*图 5：OpenSpec + Superpowers 组合方案分层架构*

## 5\. 快速选型决策表

把上面的分析压缩成一张表：

| 维度 | OpenSpec | Superpowers | 组合方案 |
| --- | --- | --- | --- |
| 核心能力 | 规格管理 + 变更追踪 | 行为约束 + TDD 强制 | 规格管理 + 行为约束 |
| 适合项目规模 | 中大型 | 个人/小型 | 中型团队 |
| 适合项目类型 | 棕地项目（已有代码库） | 绿地项目（从零开始） | 混合 |
| 上手成本 | 中（需要写规格文档） | 低（开箱即用） | 中高 |
| Token 消耗 | 低（按需加载规格） | 中高（技能文档全量注入） | 高 |
| AI 工具覆盖 | 22 个 | 5 个 | 5 个（取交集） |
| 需求变更管理 | 强（增量规格） | 弱（无专门机制） | 强 |
| 代码质量保障 | 弱（无行为约束） | 强（TDD + 审查 + 验证） | 强 |

一句话选型建议：

- **需求复杂、变更频繁、多人协作** → OpenSpec
- **一个人快速迭代、需要代码质量保障** → Superpowers
- **中型团队、从零开始、有明确需求** → 组合方案

## 6\. 模型适配实测

OpenSpec 和 Superpowers 的效果跟底层模型直接相关。Superpowers 的反合理化设计、TDD 铁律，模型不听话就白搭；OpenSpec 的 Delta Spec 编写和 DAG 依赖推理，也需要模型有足够的指令遵循能力。

本文的测试跑了两个模型。个人感觉， **智谱 GLM-5.1** 综合实力更强，生成 spec 的结构化程度、复杂 Delta Spec 的合并准确度都比 MiniMax M2.7 略好。但问题是 GLM Coding Plan 官网现在限购，而且价格涨了一倍，不太好买。

退而求其次，大部分测试用的是 **MiniMax M2.7** （MiniMax Token Plan），日常场景完全够用，性价比相对高一些。两个方案入口放这，按需自取：

- 智谱 GLM Coding Plan **（比官网直购便宜 10%）：** `https://www.bigmodel.cn/glm-coding?ic=YCG7BTU5QC`
- MiniMax Token Plan **（比官网直购便宜 10%）：** `https://platform.minimaxi.com/subscribe/token-plan?code=8nzRbxE4m1&source=link`

## 总结

OpenSpec 和 Superpowers 不是竞品关系，更像是 **不同层面的互补工具** 。

OpenSpec 解决的是"AI 不知道该做什么"的问题 - 通过结构化规格、增量变更、DAG 依赖和验证引擎，让 AI 编码工具按照明确的需求干活。

Superpowers 解决的是"AI 不知道该怎么做"的问题 - 通过 14 个行为技能、反合理化设计、TDD 强制和子 Agent 架构，让 AI 编码工具按照最佳实践干活。

如果你的项目需求清晰但变更频繁，OpenSpec 更合适。如果你一个人做项目，最大的问题是代码质量而不是需求管理，Superpowers 更实用。如果是团队协作，两者组合能覆盖从需求到实现的全链路。

说到底，工具选型没有标准答案，但有一个基本原则： **先想清楚你的核心问题是什么，再选对应的工具** ，而不是哪个 Star 多就用哪个。

如果你也在用 AI 编码工具做项目开发，你目前的工作流是什么样的？评论区说说你的经验，看看大家是不是踩了同样的坑。

**好啦，谢谢你观看我的文章，如果喜欢可以点赞转发给需要的朋友，我们下一期再见！敬请期待！**

**扫码关注，获取更多 AI 工具的实战经验和最佳实践。不错过每一篇干货！**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**微信扫一扫赞赏作者**

AI编程最佳实战「2026」 · 目录

继续滑动看下一个

术哥无界

向上滑动看下一个