---
title: "从零开始玩转循环 (Getting started with loops)【译】"
source: "https://mp.weixin.qq.com/s/lG4WU5sSykOVu4XMHtWq1g"
author:
  - "[[宝玉]]"
published:
created: 2026-07-09
description: "最近大家都在热议“设计循环 (designing loops)”，而不是简单地给你的写代码的 AI 智能体 (AI Agent) 下提示词。如果你在 X（原 Twitter）上逛一逛，想搞清楚“循环”到底是个啥，你会看到五花八门的答案。"
tags:
  - "clippings"
---
宝玉 宝玉AI *2026年7月7日 12:26*

最近大家都在热议“设计循环 (designing loops)”，而不是简单地给你的编程 AI 智能体 (AI Agent) 扔一条提示词 (prompt) 就完事。如果你在 X（原 Twitter）上花点时间，想搞清楚到底什么是“循环”，你会听到五花八门的答案。

在 Claude Code 团队，我们将“循环”定义为： **AI 智能体不断重复执行工作周期，直到满足某个预设的停止条件。** 为了方便理解，我们根据以下四个维度，对循环进行了分类：

- • 它是如何被触发的
- • 它是如何停止的
- • 它使用了哪种 Claude Code 基础指令 (primitive) **(在这里指系统内置的基础命令或核心功能模块)**
- • 哪种类型的任务最适合它

接下来，我们将带你了解这几种主要的循环类型、适用场景，以及如何在控制 token 消耗的同时，保证产出的代码质量。请记住，并不是所有任务都需要复杂的循环；建议从最简单的方案开始上手，然后根据实际情况灵活挑选这些模式。

## 回合制循环 (Turn-based loops)

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/ZlwY8rlDcFPNibh2Sjn6f9ZkGJuRUV1Etibw1gZcouibaCG6zdqH3kTcSOkmretVvYEr0iaZX7icVTnF8RAK5fyDEKTiabz1ElsTFKRsM55HdC6wA/640?from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)
- • **触发方式** ：用户输入提示词。
- • **停止条件** ：Claude 自行判断任务已经完成，或者它发现需要向你索要更多上下文信息。
- • **最佳适用场景** ：不属于常规流程或定时计划的、比较简短的任务。
- • **如何控制消耗** ：编写非常具体的提示词，并通过“技能 (Skills)”功能强化验证环节，从而减少来回交互的回合数。

你发送给 AI 的每一个提示词，其实都开启了一个由你手动主导的循环。在这个循环里，你指挥着每一个回合：Claude 收集上下文、采取行动、检查自己的工作，必要时重复这些动作，最后给你回复。我们称之为“智能体循环 (agentic loop)”。

举个例子：你让 Claude 做一个“点赞”按钮。它会阅读你的代码、进行修改、运行测试，然后把它认为没问题的成果交还给你。接着，你手动检查一遍它的工作，发现没问题或需要修改后，再写出下一条提示词。

其实，你可以把你自己手动检查的这些步骤，写进一个名为 `SKILL.md` 的文件里。这样一来，Claude 就能端到端地自行完成更多检查工作。在这个文件里，你应该提供各种工具或连接器，让 Claude 能够“看”到、衡量或与最终结果进行真实交互。 **验证的标准越量化、越具体，Claude 就越容易进行自我判断。**

例如，你可以在 `SKILL.md` 文件中这样规定：

```
--- 
name: verify-frontend-change 
description: 在宣布完成之前，端到端验证任何 UI 更改。 
--- 

# 验证前端更改 (Verifying frontend changes) 
绝不能仅仅因为代码修改成功，就报告 UI 更改已完成。必须像人类代码审查员那样进行验证： 

1. 启动开发服务器 (dev server)，并在浏览器中打开修改后的页面。 

2. 直接与更改后的内容交互。对于新增的控件（如按钮、输入框、开关）：点击它，确认状态如预期般改变，并在操作前后截图。 

3. 检查浏览器控制台 (browser console)：确保没有新增任何错误 (errors) 或警告 (warnings)。 

4. 使用 Chrome 开发者工具的 MCP **(Model Context Protocol，模型上下文协议，一种让 AI 连通外部工具和数据的标准标准)**，运行性能追踪，并审核网页核心性能指标 (Core Web Vitals)。

如果任何一个步骤失败，请修复问题并从步骤 1 重新开始 —— 绝对不要把只验证了一半的工作交回给我。
```

## 目标导向循环 (Goal-based loop /goal)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/ZlwY8rlDcFO4hOiahL9MOcn6pyzH5zJCK58Yr1VGQv2c9C8WlQfYszVm8XGzc0ECutpzpyLzNibn7KmmVg49M21RZtsibLzouSuOzuOrGPSZBo/640?from=appmsg&watermark=1#imgIndex=1)
- • **触发方式** ：实时手动输入提示词。
- • **停止条件** ：目标达成，或者达到了设定的最大尝试回合数。
- • **最佳适用场景** ：具备可验证退出标准（能明确用客观数据判断对错）的任务。
- • **如何控制消耗** ：设定非常具体的完成标准和明确的回合数上限，例如“尝试 5 次后停止”。

有时候，仅仅交互一个回合是不够的，特别是在处理复杂任务时。当 AI 智能体能够不断试错、迭代时，它们往往表现得更好。你可以通过 `/goal` 指令定义“到底什么样才算做完”，从而让 Claude 有更长的时间去持续迭代。

当你明确定义了成功标准后，Claude 就不需要自己去瞎猜什么是“足够好”并过早地结束工作。每次 Claude 试图停下来交差时，背后的评估模型都会检查你的条件，如果不达标，它会被打回去继续干活，直到目标达成，或者达到了你设定的尝试次数上限。

这就是为什么 **确定性的标准** （比如通过了多少个测试用例，或者达到了某个具体的分数门槛）会如此有效的原因。

例如：

```
# 将主页的 Lighthouse 网页性能跑分提高到 90 分或以上，尝试 5 次后停止。
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

## 基于时间的循环 (Time-based loop /loop 和 /schedule)

- • **触发方式** ：设定的时间间隔。
- • **停止条件** ：你手动取消它，或者工作彻底完成了（比如代码被合并了，任务队列清空了）。
- • **最佳适用场景** ：周期性重复的工作，或者需要与外部环境、外部系统对接的任务。
- • **如何控制消耗** ：设置更长的时间间隔，或者改为基于事件触发（而不是单纯按时间盲目运行）。

有些 AI 智能体工作是周期性的：任务本身一成不变，只是输入的数据变了。比如，每天早上汇总 Slack 聊天记录。另一些工作则依赖外部系统，与外部系统对接最简单的方式，就是每隔一段时间去检查一次，并根据变化做出反应。例如，监控一个可能会收到代码审查意见、或者未能通过 CI **(Continuous Integration，持续集成，用于自动测试和构建代码)** 的 PR **(Pull Request，代码拉取请求，即代码合并申请)** 。

对于这些场景，你可以使用 `/loop` 指令来触发 Claude，它会按照设定的时间间隔重复执行某条提示词。例如：

```
# 每 5 分钟检查一次我的 PR，处理最新的代码审查意见，并修复失败的持续集成测试。
/loop 5m check my PR, address review comments, and fix failing CI
```

需要注意的是， `/loop` 是在你本地电脑上运行的，所以一旦你关机或者退出，它就停止了。如果你想把循环搬到云端全天候运行，可以使用 `/schedule` 指令来创建一个云端的例行程序 (routine)。

## 主动式循环 (Proactive loops)

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/ZlwY8rlDcFPBufBat8tZCIgVPMWiamtG9yvZ0sWl2UXrwelUxUmwafuQgwnfDJKI86A64c9WukHnVM6RJsicIWEHiavagEIYWriaCQxEaXDqQSc/640?from=appmsg&watermark=1#imgIndex=2)
- • **触发方式** ：事件触发或定时计划，全程无需人类实时参与。
- • **停止条件** ：每个子任务在达成其具体目标时退出。但整个例行程序本身会一直运行，直到你主动将它关闭。
- • **最佳适用场景** ：定义清晰、源源不断的重复性工作流：比如用户漏洞报告 (bug reports)、工单分诊处理 (issue triage)、数据迁移、代码依赖项升级等。
- • **如何控制消耗** ：将常规的、简单的流程分配给更小、更快的模型，把能力最强的大模型留给需要做复杂判断的环节。

上面提到的那些基础指令，结合 Claude Code 的其他进阶功能（比如自动模式 auto mode 和动态工作流 dynamic workflows，目前为研究预览版），可以被组合成一个处理长期复杂任务的“超级循环”。

例如，为了处理不断涌入的用户反馈，你可以这样搭配组合：

1. 1\. 使用 `/schedule` （研究预览版）运行一个例行程序，定时检查有没有新的反馈报告。
2. 2\. 使用 `/goal` 定义任务完成的最终目标，并利用技能 (skills) 记录下应该如何验证结果。
3. 3\. 利用动态工作流 (Dynamic workflows) 来统筹多个 AI 智能体，让它们分别负责给报告分类、修复问题，以及审查代码。
4. 4\. 开启自动模式 (Auto mode)，这样整个流程就能全自动无缝运转，无需停下来等你点击确认。

把这些组合在一起，你的提示词可能会长这样：

```
# 每小时执行一次：检查 project-feedback 频道中的 bug 报告。目标：直到本次运行发现的所有报告都已被分类、处理并回复，才停止运行。在修复 bug 时，使用工作流在平行的工作区中探索三种不同的解决方案，并让一个专门作为“裁判”的模型对它们进行对抗性的严格审查。
/schedule every hour: check the project-feedback channel for bug reports. /goal: don&#x27;t stop until every report found this run is triaged, actioned, and responded to. When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.
```

## 保持代码质量 (Maintaining code quality)

一个循环产出成果的质量，很大程度上取决于围绕它建立的外围系统。在设计这个系统时，请遵循以下原则：

- • **保持代码库本身的整洁** ：Claude 会不知不觉地模仿你代码库中已有的模式和规范。底子好，它写出来的代码就好。
- • **给 Claude 提供自我验证的方法** ：通过 技能文档 (Skills) <sup>[1]</sup> 功能，把你和团队眼中的“优秀代码标准”写成规则，让它自己去对照。
- • **让文档触手可及** ：各种编程框架和代码库的官方文档里，都藏着最新、最好的实践经验。确保你的 AI 能够轻松访问这些资料。
- • **使用第二个智能体来进行代码审查** ：找一个没有被历史对话污染、拥有全新上下文的智能体来做代码审查。它的偏见更少，也不会被主干智能体的思路“带偏”。你可以使用内置的 `/code-review` 技能，或者针对 Github 的专用审查工具 (代码审查文档 <sup>[2]</sup>)。

当某一次执行的结果没达到你的标准时， **千万别仅仅停留在“把这个 bug 修好”就完事了。** 试着把这次踩坑的教训提炼出来，固化到你的规则里，从而在未来的无数次迭代中改善整个系统。

## 控制 Token 消耗 (Managing token usage)

为了有效控制 Token 消耗 **(Token 是大语言模型处理文本的基本计费单位，类似按字数算钱)** ，你的循环必须有清晰的边界：

- • **选择合适的指令和模型** ：杀鸡焉用牛刀。小任务根本不需要动用多个智能体或复杂的循环。很多任务用更便宜、更快的模型就能完美解决。
- • **定义明确的成功与停止标准** ：非常具体地描述出“完成”到底是个什么状态，这样 Claude 就能更快地找到答案（当然，也不能快到敷衍了事）。
- • **在大规模运行前先“试水”** ：动态工作流可能会一下子衍生出几百个智能体。在大规模部署前，请先切出一小块工作，测试一下实际的消耗量，心里有个底。
- • **用脚本处理确定性的工作** ：直接运行一段脚本，比让大模型一步步去逻辑推理要便宜得多。例如，处理 PDF 的技能可以直接内嵌一个填写表单的脚本，每次让 Claude 跑这个脚本就行，而不是每次都让它绞尽脑汁重新推导代码该怎么写。
- • **别把例行程序跑得太频繁** ：你监控的事物多久变一次，你的检查间隔就应该设为多长。不要让 AI 傻傻地每秒钟去刷新一个一天才更新一次的网页。
- • **定期查看消耗** ：输入 `/usage` 命令，它可以按技能、子智能体 (SubAgents) 和 MCP 详细拆解近期的消耗情况；直接输入不带参数的 `/goal` ，可以查看目前跑了多少回合以及 Token 的消耗量； `/workflows` 会显示每个智能体的具体 Token 消耗，并且你可以在那里随时让某个智能体停下来。

## 开始你的探索之旅 (Getting started)

简单总结一下：

| **循环类型 (Loop)** | **你需要移交什么 (You hand off)** | **适用场景 (Use it when)** | **所需工具 (Reach for)** |
| --- | --- | --- | --- |
| 回合制 (Turn-based) | 检查工作 (The check) | 你正处于探索或决策阶段 | 自定义验证技能 |
| 目标导向 (Goal-based) | 停止条件 (The stop condition) | 你明确知道“完成”的标准是什么 | `/goal` |
| 基于时间 (Time-based) | 触发器 (The trigger) | 工作在你的项目之外按时间表发生 | `/loop`  , `/schedule` |
| 主动式 (Proactive) | 提示词 (The prompt) | 循环往复且定义极其明确的工作 | 以上全部，外加动态工作流 |

想要开始尝试循环，不妨先审视一下你日常手头的工作。挑一个你总是成为效率“瓶颈”的任务，然后问问自己： **我能把哪一部分交接给 AI？**  
我能写出自动验证的检查项吗？任务目标足够清晰吗？这项工作是不是定时发生的？

一旦你有了思路，就把循环跑起来！仔细观察结果，看看它在哪里卡壳了，或者在哪里用力过猛了， **不要害怕去不断迭代和优化它** 。

欲了解更多进阶信息，请阅读 Claude Code 的官方文档：AI 智能体基础 <sup>[3]</sup> ，以及 目标设定 (/goal) <sup>[4]</sup> 、例行程序 (/routines) <sup>[5]</sup> 和 动态工作流 (workflows) <sup>[6]</sup> 的相关专题页面。

---

本文由 @delba\_oliveira 撰写。

https://x.com/ClaudeDevs/status/2074208949205881033

#### 引用链接

`[1]` 技能文档 (Skills): *https://code.claude.com/docs/en/skills*  
`[2]` 代码审查文档: *https://code.claude.com/docs/en/code-review*  
`[3]` AI 智能体基础: *https://code.claude.com/docs/en/agents*  
`[4]` 目标设定 (/goal): *https://code.claude.com/docs/en/goal*  
`[5]` 例行程序 (/routines): *https://code.claude.com/docs/en/routines*  
`[6]` 动态工作流 (workflows): *https://code.claude.com/docs/en/workflows#orchestrate-subagents-at-scale-with-dynamic-workflows*

阅读原文

同步

点击同步文章到多平台