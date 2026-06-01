---
title: "Harness Engineering：让 AI 帮你写代码的正确姿势"
source: "https://mp.weixin.qq.com/s/nYc0xsrLamNXmJBI-jZgIA"
author:
  - "[[一川]]"
published:
created: 2026-06-01
description: "你不需要让马变得更聪明。你需要给它更好的缰绳。AI Coding也不需要LLM越聪明，但需要你给他配备好完善的运行环境、工具、技能、约束规则等。"
tags:
  - "clippings"
---
一川 *2026年4月5日 11:57*

> 你不是在编写智能，你是在构建智能运行的世界。

如果你最近关注 AI 编程领域，一定听过一个越来越火的词—— **Harness Engineering** （约束工程）。2025 年是 AI Agent 证明自己能写代码的一年，而 2026 年，我们学到了一个更深刻的教训： **Agent 不是难点，Harness 才是。**

这篇文章会用最通俗的方式，带你理解什么是 Harness Engineering，为什么它如此重要，以及如何用 Claude Code 实践它。即使你从未用过 AI 编程工具，读完也能上手。

---

## 一、从一个真实的痛点说起

假设你正在用 AI 编程助手（比如 Claude Code、Cursor、Codex）开发一个项目。你兴奋地输入一条指令：

```
帮我用 Next.js 搭建一个博客，要有文章列表、标签筛选、暗色模式。
```

AI 开始工作了。它读文件、写代码、装依赖，看起来很专业。

但过了一会儿你发现——

- 它用了你项目里根本不用的 CSS 框架
- 命名风格跟你现有代码完全不一致
- 它改了一个文件，结果把另一个功能搞坏了
- 你让它"改一下样式"，它把整个页面重写了

**听起来熟悉吗？**

这不是 AI 不够聪明。事实上，当今的大语言模型（如 Claude、GPT）已经非常强大。问题出在： **你没有告诉它"在什么环境里、按什么规则工作"。**

这就是 Harness Engineering 要解决的问题。

---

## 二、什么是 Harness Engineering？

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 2.1 一个类比：赛马与缰绳

"Harness"这个词来自马具——缰绳、马鞍、马嚼子——一整套用来引导强大但不可预测的动物朝正确方向奔跑的装备。

这个比喻很精确：

| 比喻 | 对应 |
| --- | --- |
| 马 🐎 | AI 模型（Claude、GPT 等） |
| 缰绳 🪢 | 约束和规则（CLAUDE.md、lint、类型检查） |
| 跑道 🏟️ | 项目环境（目录结构、技术栈、依赖） |
| 骑师 🧑 | 你（制定方向、审查结果） |

马很强壮、很快，但它不知道该往哪跑。骑师的工作不是替马跑步，而是给它方向和边界。

同样， **Harness Engineering 就是设计 AI Agent 运行的"世界"——约束、反馈循环、文档、验证机制——让 AI 可靠地完成工作。**

### 2.2 正式定义

用一句话概括：

> **Agent = Model + Harness**

- **Model（模型）** ：AI 的"大脑"，负责理解需求、推理、生成代码
- **Harness（套具）** ：模型之外的一切——工具、规则、上下文、反馈循环、安全护栏

你无法让模型变得更聪明（那是 Anthropic、OpenAI 的工作），但你可以通过构建更好的 Harness，让同一个模型表现得更出色。

一个来自 LangChain 的真实数据：他们的编程 Agent 在 Terminal Bench 2.0 基准测试中，仅通过改进 Harness（模型完全不变），得分从 52.8% 跳到了 66.5%，直接从第 30 名冲进前 5。

**同一匹马，不同的缰绳，天壤之别。**

---

## 三、Harness 的核心组成部分

一个完整的 Harness 通常包含以下几个层次：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 3.1 上下文层（Context Layer）

AI 只能看到你放在它面前的东西。那些存在于 Slack 聊天记录、Google Docs、或你脑海中的知识，对 AI 来说等于不存在。

上下文层的核心工具是 **CLAUDE.md** （在 Claude Code 中）或 **AGENTS.md** （在 Codex 中）。它是一个放在项目根目录的 Markdown 文件，告诉 AI：

- 这是什么项目？
- 技术栈是什么？
- 目录结构长什么样？
- 有哪些编码规范？
- 有哪些禁止事项？

以下是一个实际的 `CLAUDE.md` 示例：

```
# My Blog — 项目上下文

## 概述
一个使用 Next.js 15 构建的个人技术博客。
内容以 MDX 格式存储在 /content/posts/ 目录下。

## 技术栈
- Next.js 15 (App Router)
- TypeScript (严格模式)
- Tailwind CSS v4
- MDX 用于内容
- 部署到 Vercel

## 目录结构
- src/app/          → 页面和布局
- src/components/   → 可复用组件
- src/lib/          → 工具函数、MDX 处理
- content/posts/    → 博客文章（.mdx 格式）
- public/           → 静态资源

## 编码规范
- 使用函数式组件 + TypeScript interface
- 组件放在 src/components/，PascalCase 命名
- 仅使用 Tailwind 工具类，不写自定义 CSS 文件
- 每篇文章的 frontmatter 必须包含 title, date, description, tags
- 所有图片使用 next/image
- 组件超过 150 行必须拆分

## 常用命令
- npm run dev       → 启动开发服务器
- npm run build     → 生产环境构建
- npm run lint      → ESLint 检查
- npx tsc --noEmit  → 类型检查

## 禁止事项
- 禁止使用 any 类型
- 禁止在提交代码中保留 console.log
- 禁止修改 package.json 而不说明原因
- 禁止删除现有测试而不提供替代方案
```

**为什么这么重要？** 因为没有这个文件，AI 每次开始工作时都在"猜"你想要什么。有了它，AI 第一时间就知道上下文和边界。OpenAI 的团队在实践中发现，与其把 AGENTS.md 当成百科全书，不如把它当成 **目录** ——指向更详细文档的入口。

### 3.2 技能层（Skills Layer）

Skills（技能）是一种 **渐进式披露** 机制。与其把所有指令都塞进 CLAUDE.md，不如把特定任务的详细流程拆分成独立的 Skill 文件，让 AI 在需要时才加载。

这解决了一个现实问题：上下文窗口是有限的。如果你把所有规则都塞进系统提示，AI 反而会变差——关键信息被淹没了。

举个例子，你可以创建一个"新建博客文章"的 Skill：

```
<!-- .claude/skills/new-post.md -->

# 技能：创建新博客文章

## 何时使用
当用户要求创建新的博客文章或文章时。

## 执行步骤
1. 询问文章信息：标题、描述、标签
2. 根据标题生成 slug（kebab-case 格式）
3. 在 content/posts/{slug}.mdx 创建文件
4. 包含标准 frontmatter 模板：
   ---
   title: "文章标题"
   date: "YYYY-MM-DD"
   description: "文章描述"
   tags: ["标签1", "标签2"]
   published: false
   ---
5. 生成包含 h2 章节的内容骨架
6. 验证文章能否正常渲染：运行 npm run dev
```

**关键思维转变** ：你不是在教 AI 怎么编程（它已经会了），你是在告诉它 **你的项目里怎么做事** 。

### 3.3 护栏层（Guardrails Layer）

这是安全工程与 Harness Engineering 的交汇点。护栏确保 AI 的每一步操作都在可控范围内。

在 Claude Code 中，Hooks 是实现护栏的主要机制——在 Agent 生命周期的关键节点自动执行脚本：

```
// .claude/settings.json
{
  "hooks": {
    "preCommit": [
      "npx tsc --noEmit",
      "npm run lint"
    ]
  }
}
```

这意味着 Claude Code 在每次提交代码之前， **必须** 先通过类型检查和 lint 检查。如果失败，就不能提交。

更完整的护栏体系包括：

```
提交前护栏（Pre-commit）
├── TypeScript 类型检查 → 确保类型安全
├── ESLint 检查          → 确保代码风格一致
├── 构建检查             → 确保项目能正常构建
└── 敏感信息扫描         → 确保不提交 API 密钥等

运行时护栏（Runtime）
├── 文件访问控制         → 限制 AI 只能修改特定目录
├── 破坏性操作审批       → rm -rf 等需要人工确认
└── 依赖安装审查         → 新增依赖需要说明原因
```

### 3.4 验证反馈循环（Verification Loop）

这是 Harness 最容易被忽略但最有价值的部分。没有反馈循环，AI 会说"我觉得没问题"；有了反馈循环，AI 必须证明"测试通过、lint 干净、类型检查通过"。

```
写代码 → 运行测试 → 检查 lint → 类型检查 → 构建验证
  ↑                                              |
  └──────────── 失败则修复并重试 ←────────────────┘
```

在 Claude Code 中，你可以在 CLAUDE.md 的"质量门禁"部分定义这个循环：

```
## 质量门禁（每次提交前必须通过）
1. \`npx tsc --noEmit\` 必须通过
2. \`npm run lint\` 必须通过
3. \`npm run build\` 必须成功
4. 不允许提交包含 console.log 的代码
```

---

## 四、动手实践：用 Claude Code 搭建一个博客

现在让我们把理论变为实践。以下是完整的操作步骤。

### 4.1 安装 Claude Code

在 macOS 终端运行：

```
# 安装 Claude Code（原生安装，无需 Node.js）
curl -fsSL https://cli.claude.com/install.sh | sh

# 验证安装
claude --version
```

首次运行 `claude` 命令后，会打开浏览器进行 OAuth 认证。你需要一个 Pro（100/月）订阅。如果你已经有 Claude 的 $20 订阅， **你已经可以使用 Claude Code 了** 。

当然，你也可以配置其他LLM的Coding Plan，比如说GLM、MiniMax等，这里可以推荐一个Claude Code的可视化配置工具cc-switch（https://github.com/farion1231/cc-switch），可以让你随时切换LLM。

![choose](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 4.2 创建项目并初始化 Harness

```
# 创建项目目录
mkdir my-blog && cd my-blog

# 启动 Claude Code
claude
```

进入 Claude Code 后，输入你的第一条指令：

```
初始化一个 Next.js 15 博客项目，使用 App Router + TypeScript + Tailwind CSS。
支持 MDX 渲染博客文章。创建首页文章列表和文章详情页。
```

Claude Code 会自动完成以下工作：

- 运行 `npx create-next-app@latest`
- 安装 MDX 相关依赖
- 创建页面路由和组件
- 设置 Tailwind 配置

### 4.3 创建 CLAUDE.md

这是搭建 Harness 的第一步，也是最重要的一步。在 Claude Code 中输入：

```
在项目根目录创建 CLAUDE.md，包含以下内容：
项目概述、技术栈、目录结构、编码规范、常用命令、质量门禁和禁止事项。
参考项目当前的实际结构来写。
```

Claude Code 会根据刚才创建的项目结构，自动生成一个准确的 CLAUDE.md。

> 💡 **小技巧** ：CLAUDE.md 应该简洁有力，不超过 60 行，最多不要超过500行。把它当成"目录"而不是"百科全书"。如果某个主题需要详细说明，放到单独的文档中。

### 4.4 创建 Skills

```
# 在 Claude Code 中输入
创建 .claude/skills/ 目录，并创建以下三个 skill 文件：
1. new-post.md - 创建新博客文章的标准流程
2. new-component.md - 创建新 React 组件的标准流程
3. pre-deploy.md - 部署前检查清单
```

每个 Skill 文件的结构都遵循相同模式：

```
# 技能名称

## 何时使用
描述触发条件

## 执行步骤
1. 第一步
2. 第二步
3. ...

## 验证标准
- 如何确认这个任务完成了
```

### 4.5 建立验证机制

```
# 在 Claude Code 中输入
帮我在项目中配置以下验证机制：
1. ESLint 配置 strict 规则
2. TypeScript strict mode
3. 添加一个 pre-commit 检查脚本
4. 在 CLAUDE.md 中添加质量门禁章节
```

### 4.6 创建进度追踪文件

```
<!-- progress.md -->
# 开发进度

## 已完成
- [x] 项目初始化
- [x] CLAUDE.md 创建
- [x] Skills 配置
- [x] 首页文章列表

## 进行中
- [ ] 文章详情页 + MDX 渲染

## 待开发
- [ ] 标签筛选
- [ ] 暗色模式
- [ ] RSS 订阅
- [ ] SEO 优化
```

这个文件的价值在于：当你开启新的 Claude Code 会话时，Claude 会自动读取它和 CLAUDE.md，瞬间了解项目状态并从中断处继续。

---

## 五、Harness Engineering 的核心原则

通过以上实践，我们可以提炼出几条核心原则：

### 原则 1：约束解放生产力

这听起来矛盾，但约束实际上让 AI 更高效。当 AI 可以生成任何代码时，它会浪费 token 探索死胡同。当 Harness 定义了清晰的边界，AI 会更快收敛到正确方案。

**没有 Harness** ：AI 自由发挥，风格混乱，需要反复修改 **有 Harness** ：AI 在规则内高效输出，一次到位

### 原则 2：仓库即知识库

把所有项目知识放进仓库——而不是聊天记录、Slack 消息、或你的脑子里。

```
❌ 你在 Slack 里说："咱们用 Tailwind 不用 CSS Modules"
✅ 你在 CLAUDE.md 里写："仅使用 Tailwind 工具类，不写自定义 CSS 文件"
```

AI 只能看到仓库里的东西。任何它不能在上下文中访问的知识，对它来说等于不存在。

### 原则 3：失败驱动改进

当 AI 犯错时，不要只修复输出——要 **工程化地防止同类错误再次发生** 。

```
第一次：AI 提交了带 console.log 的代码
  → 修复：删掉 console.log ❌（治标不治本）
  → 改进：在 lint 规则中禁止 console.log ✅（永久解决）

第二次：AI 用了 any 类型
  → 修复：手动改成正确类型 ❌
  → 改进：在 CLAUDE.md 禁止事项中加入"禁止使用 any" ✅
```

### 原则 4：保持 Harness 轻量

不要过度工程化。OpenAI 的团队给出的建议是：

- **YAGNI** ：不需要的东西不要提前构建
- **先简单再优化** ：写最直接的方案，有问题再改
- **大胆删除** ：代码越少，bug 越少

一个好的 Harness 应该是可以随时"撕掉重建"的。模型在快速进步，今天需要复杂管控的地方，明天可能一个提示就能搞定。

---

## 六、从 Vibe Coding 到 Harness Engineering

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

AI 编程的发展经历了三个阶段：

| 阶段 | 时间 | 特征 | 类比 |
| --- | --- | --- | --- |
| Vibe Coding | 2024-2025 | 凭直觉写提示词，看 AI 自由发挥 | 放开缰绳让马自己跑 |
| Spec Coding | 2025 | 写详细规格说明，逻辑约束 | 给马画一条路线 |
| Harness Engineering | 2026 | 构建完整运行时环境 | 给马装上全套马具 + 跑道 + 裁判 |

Vibe Coding 很有趣，但不可靠。Spec Coding 更好，但 AI 仍然可能偏离规格。Harness Engineering 是系统性的解决方案——你不仅告诉 AI "做什么"，还构建了一个 **确保它做对** 的环境。

---

## 七、你的 Harness 清单

如果你想现在就开始实践 Harness Engineering，以下是一个最小可行清单：

```
## 最小可行 Harness

□ CLAUDE.md / AGENTS.md
  - 项目概述（3-5 句话）
  - 技术栈（列出关键依赖）
  - 目录结构（主要目录说明）
  - 编码规范（5-10 条最重要的规则）
  - 常用命令
  - 禁止事项

□ 至少 1 个 Skill
  - 你最常执行的重复性任务

□ 基础护栏
  - TypeScript strict mode
  - ESLint 配置
  - 提交前自动检查

□ 进度文件
  - progress.md 记录已完成 / 进行中 / 待开发
```

不需要一步到位。先从 CLAUDE.md 开始，遇到问题时再逐步添加 Skill 和护栏。记住那条黄金法则： **当 Agent 犯错时，工程化一个方案让它不再犯同样的错。**

---

## 八、结语

Harness Engineering 不是什么高深的技术。它的本质是一种思维方式的转变：

**从"写代码"到"构建 AI 写代码的环境"。**

最好的 AI 产品不是拥有最强模型的团队做出来的，而是拥有最成熟 Harness 工程实践的团队做出来的。模型是可替换的零件，Harness 才是真正的产品。

如果你正在使用 Claude Code、Cursor、Codex 或任何 AI 编程工具，今天就开始：

1. 为你的项目创建一个 CLAUDE.md
2. 把你脑海中的编码规范写下来
3. 添加基础的 lint 和类型检查
4. 当 AI 犯错时，把修复变成规则

**你不需要让马变得更聪明。你需要给它更好的缰绳。**

---

*最后，越来越多公司在演进升级AI Coding姿势，古法编程的时代已经终结，传统的珍妮机正在被蒸汽机给取代。希望大家都能持续学习、无限进步，拿到进入AI新时代的船票。*

收录于AI Coding

继续滑动看下一个

宇宙一码平川

向上滑动看下一个