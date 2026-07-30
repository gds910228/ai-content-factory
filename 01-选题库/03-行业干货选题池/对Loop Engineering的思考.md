---
title: "对Loop Engineering的思考"
source: "https://mp.weixin.qq.com/s/g3HtSeJfKfjtqDG4rPTpiw"
author:
  - "[[吕昊俣]]"
published:
created: 2026-07-30
description:
tags:
  - "clippings"
---
吕昊俣 腾讯云开发者 *2026年7月30日 08:45*

关注腾讯云开发者，一手技术干货提前解锁👇

OpenClaw 的创始人在 6月8日 凌晨 2:58 发布推文： Here's your monthly reminder that you shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents.”。简单翻译一下就是：我们要设计一个循环去代替不停地Prompt，把人从流程中拔出来。loop是不是又是AI圈造了一个新词，不清楚，但是确实给我们看待“问题”提供了一个新的视角。

## 01

范式迁移：从 Harness 到 Loop 再到Graph Engineering

**1.1 五代工程演进**

从 2022 到 2026，AI 辅助编程经历了清晰的开发 **模式的转移** 。

工程师的核心工作，逐渐从 **“直接写业务代码”** 转向 **“设计系统，并让系统生成代码”** 的阶段。

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr7ibViczAfdicicAUxnpN9LVxeicl0w7KLlQibvsHLLZChbPqelo6nic3t7JUYbOZibLjXJSHAic7DTXpKVM1SFUdfpXicooIrSydXicvic5lg/640?wx_fmt=png&from=appmsg#imgIndex=0)

每一代都是一次 **精进** ：

1. **Prompt Engineering** （2023）解决了“怎么问，模型才答得好”，把质量押在一次提示词上。缺点是：答错了没有自动纠偏，只能人工重来。
2. **Context Engineering** （2025）解决了“模型缺背景、答不准”，上下文管理让信息更充分。缺点是：只有信息、没有手脚，缺标准化执行环境，也缺验证闭环。
3. **Harness Engineering** （2026 2月）解决了、“单次执行不可控、不可信”，生产级运行外壳让 Agent 能安全、可控、可验证地跑通一次。缺点是：仍要人触发、让人盯，人成了生产节点的最大瓶颈。
4. **Loop Engineering** （2026 6月）解决了“ **靠人盯”** ，自动化调度实现最大限度的无人值守，但仍面临着成本失控的问题。
5. **Graph Engineering** （2026 7月）解决了“Loop间的编排、协同、调度等问题”，构建起工程级复杂 AI 任务系统。

**1.2 它们的结构关系：层层依赖 逐步递进**

每一次的演进， **并不是一次替代** ，而是建立在上一代的能力之上。

就拿Harness和Loop的关系来说，创始人Addy Osmani 给出了精准的概括：

**Harness 是 AI 代理的受控运行环境；Loop 是在这个环境之上，叠加了自驱动能力的持续执行流程。**

Harness 是地基，Loop 是上层调度，没有Harness，Loop 则是无源之水。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr4cdH7IIsr8QSNq9ibkwUFk5nokFScVAWOxc1NzEGqzdUib3Rc62ibzmu5ftsm83MUdWHNfHwpHXmrLEicIXnJwJETDY9SUqslI1lA/640?wx_fmt=png&from=appmsg#imgIndex=1)

而把它们结合在一起看，更为直观明了。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr6xWB8dXY84FzdHiaxiaZyFJDXeibFR2WrVrFhxIj68g0xAYXBT9mQ4DFXoQ15iaczLpEYwoSaYRNbLewnhzzqEHVJ5QvHZ2ICMxkc/640?wx_fmt=png&from=appmsg#imgIndex=2)

**1.3 从技术Loop到产品Loop**

跳出单纯的技术视角， **吴恩达** 则给出了不同的 **“取景框”** ，把 Loop 的涉众范围扩大去思考。

（见：https://www.deeplearning.ai/the-batch/three-key-loops-for-building-great-software）

文中给出了三个环： **技术->产品->用户，** 它们 **三层嵌套、不同速度、层层驱动** 。

**技术 Loop** 解决的是 “系统会不会收敛、会不会停、会不会认错”；

**产品 Loop** 解决的是 “这个闭环是否持续创造用户价值、是否值得继续放大、是否能形成长期增长飞轮”。

**用户Loop** 则反应了用户对产品的一种 **”情绪“** ，最终将以 **某种形式** 回到产品本身。

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr6EtDRibs9MrCorBnchZTjmpsAH4T8Df0T2YXqhjW7sfIzbos1uZFJMibmyghvS1HnzWLAeZb4ELoJAhibEic88WwzyNl35OMMxao4/640?wx_fmt=png&from=appmsg#imgIndex=3)

**1.4 Loop的工程基础: 控制论**

大约160年前，英国通过了《红旗法案》，此法案要求机动车 **前必须有人持红旗引导** ，以保护人的安全，是不是有点匪夷所思，但160年后的今天，在AI编程领域， **历史在重演** ，人就站在AI的前头，时时刻刻盯着。一个字: 累。

从原理上看，LLM是一个概率模型，本质上，它就是在： **猜** 。

虽是猜，但有人会说，现在猜的已经很准了，正确率接近 **90%** 。

是的，90%听起来很不错，但是，事实上可能很糟糕，因为，软件工程一定会使用 **分治的方法** 解决复杂问题，顺其自然的，一个复杂任务就变成了N多子任务的叠加，那么就变成了一个指数运算，仅仅六次后，概率就接近50%， 这不是就是 **抛硬币吗** ！

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr5BPykvExU3PTPhoaG2AHD9H8OKdEogwEv3LvmJcvobgC9Zr75ibA2Whk8XcumPSx5SBxYKSRIKfvszWAIuElz2fd7Uz4bc1nbI/640?wx_fmt=png&from=appmsg#imgIndex=5)

为了解决这个问题，于是乎，很自然地就想，有没有一种机制可以 **修正这个损失概率？** 有，这种机制就是控制论。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr681QicvRYicYETww6BpZibiciaFSoGdLlQKELOg3RYYQ5nRTU7hrUhhS0yzAUybYLibiaiaUJwUs3bCyQn4AdBRM0DlEJ2Ido59rwLqyg/640?wx_fmt=png&from=appmsg#imgIndex=6)

而控制论的思想，早从 **VibeCoding** 时，我们就在每天下意识的使用它。

只是这个 **系统=我+AI** ，比如在构建Prompt的过程：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7fTWUFMndWFgEv5Xw1SCoUKNgsDdYYRt0Jhbo4Ewsybz1I8uS0TzGDP86ZjTj9NDL6hyB3hiaCb97zffgrfeq60cYyeUKPjdFY/640?wx_fmt=png&from=appmsg#imgIndex=7)

而控制论的本质一句话就可以说明白 **：通过负反馈机制去收敛目标函数。** 说白了，Loop Engineering就是控制论在AI领域的一次落地应用。

**1.5 控制论四大公理**

于是乎，最近又翻开了大学时候没有好好上的课程： **《反馈控制系统设计》** ，温习了一下控制论中最基本的几点思想：

1. **构建负反馈闭环**
2. **可观测性**
3. **可控性约束**
4. **离散迭代纠偏**

而这些点，更好的帮助我去理解Loop Engineering，我会清晰的看到，它们 **一一对应，同根同源** 。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7HkyBbtbhEyHU6wunglnpTKcNeyp1ZcQv49BruLXb9eYqH2epJtz9ibhTT5E3z76ALzxcZ3soVVQGEoSuCg3PEZZpOoHhSicgAI/640?wx_fmt=png&from=appmsg#imgIndex=8)

映射如下：

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr57jL38HBTlPTehsdPDypzic3ZnFqhqGJnJfIQexgm1lBIpkuhsgVXEjJDmYc1qBz2rMBxe4htHkNbbiaofWbGjCSPAhwicKO4FvI/640?wx_fmt=png&from=appmsg#imgIndex=9)

## 02

从“写Prompt” 到 “设计Loop”

**2.1 回到问题本身：要设计一个“无人值守”的系统，咋做？**

我常常有这样的期待：一个任务，在晚上睡觉前 设计好，我睡觉，他干活，早上起来，完事。但现实往往是早上起来一看，什么东西！借助Loop的思维，我们如何重新思考这个问题？让AI可以在一定的成本下 完成任务。我想这里关键的实践路径是： **从小闭环做起，不断扩展边界**

在设计一个Loop的时候，我们往往会陷入到一个惯性思维里：

一上来就像做 **一个全自动开发、全自动修复** 的万能循环，结果往往差强人意。而比较实现的做法是：

**先跑通一个最小可收敛闭环，再逐步放大自治边界，并从中建立起闭环和闭环之间的联系。把小闭环跑通，才有资格谈大闭环，大循环是在一个个小循环上长出来的。**

而不管是大小闭环，最核心的是想清楚下面几个问题：

1. 如何定义 **问题** ？
2. 如何定义 **开始** ？
3. 如何设计 **反馈** ？
4. 如何定义 **结束** ？

**“设计反馈”** 的背后是说，你需要设计一个 **机制** ，让模型真的会 **说“不”** ，这种“不” 并不是在提示词里一些拒绝意图的Prompt，这种看似在否定，但其实还是在肯定，而这种“不”是基于 **某种不可否认的事实** ，而从这种不，就天然形成了最关键的 **“负反馈”** 链路。

**“如何结束”** 的背后是说，你需要设计一个 **机制** ，保证不会 **无限循环** ，看看你的Token账单，你知道我在说什么吧。

按我们带着以上的问题，看看官方的 **参考答案** 如何。

**2.2 五大组件+记忆模块**

在《Loop Engineering 循环工程》（https://addyosmani.com/blog/loop-engineering/）一文中，详细讲解了这几个部分，如下图所示：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr6SORqkHhvVdkSIMq7QvuY1LFicLcyTTHicqbYruAsLCAU7fgXLRciaFghXwE0bibSfVe1KuKUeudhW3QNIibgwz7Bia3ibzQ0Wnp6xtY/640?wx_fmt=png&from=appmsg#imgIndex=10)
1. **一个唤醒机制： Automations**
	以往和AI协作， **是我推一下，它动一下** 。讲道理，很累人。一个唤醒机制就保证了，人不用再去 **“盯着，去喊”，** 这是整套自动化系统运行的前提。
2. **安全独立的沙箱环境： Worktrees**
	多Agent协同必然会变成一种趋势，为每个任务分配独立代码工作区，就杜绝文件覆盖、环境互相污染等问题。
3. **对抗性思维：Maker-Checker 双校验模式**
	Maker-Checker模式本质上就是保证了： **让模型不要自说自话** ，采用 **“一方做、一方质疑”** 的制衡思路，结合Skills的经验库。二者互补修正，大幅提升输出质量。
4. **通信模式：Connectors**
	作为一种系统间的沟通手段，比如MCP、Functioncall等等，就是为了打通所有的上下游系统，把系统链接起来，
5. **长任务记忆系统： Memory**
	防止任务“失忆”。长流程任务没法全塞进 AI 有限上下文里，记忆组件会全程记录任务进度、过往尝试，防止多轮迭代后系统忘记目标、丢失执行记录。

## 03

如何让模型说“不”？

**3.1 方法一：践行TDD！！！**

让模型说“不”，最关键就是 **有硬性** 的 **不可怀疑** 的证据。

而在软件工程中，测试不过就是铁的依据。

因此，AI时代，我们需要重新思考： **TDD的价值以及如何实践？**

而从Loop的视角重新看TDD，我们会发现：

TDD的价值并不是多写几个测试用例，而是， **可以把需求翻译成反馈信号** 。

这做到这里的前提，就是：落实TDD **左移** 。

多少次实践中，我也常常会等到开发完之后，再给AI补一句： **请补充测试用例。**

而这种习以为常的习惯，其实已经 **偏离** 的TDD的本质。

所以，我们有必要在回看一下TDD的理念： **先定标准、后做开发、以结果反向驱动过程** 。

构建出一个最小的Loop **：Red-Green-Refactor**

- **红** ：先编写失败测试用例，定义" **什么是错、什么是对"** 的终态标准。
- **绿** ：迭代编写代码，直到全部测试用例通过。
- **重构** ：在测试兜底前提下优化代码，保证质量不退化。
![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr4hGHic2hA2CADMTMKwLY297PxOhKhibQCZ1Okibia5IUJOHAvEyibep2PAoYWZiazVXTpcSMZ0I4tf9TvtO7qPfYVVrWL2ZicsY0FxfM/640?wx_fmt=png&from=appmsg#imgIndex=11)

以往这个循环为什么玩不起来，因为，这个循环的控制者是人，但是到了AI时代， **控制权交给Agent** ，这个结构没有发生变化，但是你变轻松了。

在分布式系统中，每个服务都是全局中的一个局部，针对局部的一个模块，测试会有三个维度，也分别对应着三个环：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr6OkTvjuvLnx90ianSibxREbBAsF4hB3zcKdQRJ1vQUVXRG8EJvxm4MZIgkUYShPxxAzYr0p8Qn5bQssZjob5ox0IqQA7iaaQbzibE/640?wx_fmt=png&from=appmsg#imgIndex=12)

1、 **单元测试环** ：看似容易，其实不容器做到，这里难点在于：单元测试其实是和函数耦合的，也就是说，需要先定义好骨架，顾开发的流程应该是： **定义桩函数-> 写测试用例->写实现 。**

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr5pZNjsmnYtc4W9z7nWDhzb9xR3gR0zfZKjUxqd6ibItzGAFvFxBGBO4iaicN6773poV4PtvP0MCiaSM0t4oMZpCS1RYNl6ve0IGXc/640?wx_fmt=png&from=appmsg#imgIndex=13)

2、 **接口测试环** ：需要可以让AI可以自己发包，以及收日志，这样就可以在服务维度建立Loop。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr66RF5kWia7oPgXl4qItyUSocugFHOA0bKkXdNxWG6xDkq2aicsJ6XeBo7SgmHC8vHTYSgaWH9CCubwyib63sYyxdmYsRpNp5uHTM/640?wx_fmt=png&from=appmsg#imgIndex=14)

3、 **流程测试环** ：以功能为单位进行验证，因为它更加上层，一般都是用来回归验证，如何构建这个环，以便AI可以站在全局修复问题，仍然值得思考。

**3.1.1 反向思考：TDD不能做什么？**

虽然TDD好，但，也不是万能药，我们需要清晰的知道它的边界：

它 **适合** ：

- 明确的业务规则
- API的输入、输出行为
- 数据转换和边界条件
- 回归Bug修复
- 编译、lint、类型检查

它 **不适合** ：

- 纯体验问题
- 架构品味
- 产品决策

知道了 **适不适合** ，就可以更好的思考，它 **应该被放在哪里** ？

在开发过程中，我们都应该反问自己： **这个功能是否可以被测试表达？这部分如何变成Loop？**

**3.1.2 以“规则”为核心的构建测试用例**

上面我们主要讲了如何构建环？下面来讲讲如何设计测试用例。

测试用例的设计非常重要！！！因为一旦设计有误，所有AI生成的代码都是在错误的基础上改动代码，结果怎么改都是错。

而这里的解决思路是： **以需求为出发点，构建规则集合。**

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr7tcUkOltPM67XbXvPy7NuJ8BUsq6iaVzkzkTXHEUKDaznHVp5PiaVFrpsopoKAtiap5hU4hRx9lPXia40s1JBnT3z2PbeRYKPKiaV0/640?wx_fmt=png&from=appmsg#imgIndex=16)

**3.2 方法二： 证据胜于一切，建立证据链**

Maker-Checker双校验架构听起来是很不错的，但是细想，一个问题很自然的就出来了： **Checker凭什么就说Maker做的不行呢？是靠猜吗？肯定不是。**

这很像是一场辩论赛，反方选手说你不行，那不能靠感觉，要靠依据，那依据是什么呢？没事，是 **证据链** 。

Maker 通过事实（产品规则）推演，输出落地代码。

Cherker 使用 **证据链** 进行追溯，Review代码。

而这种设计，本质上就是 **对抗性思维** 的一种极致体现！

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7V8p6WRTJdUR6pRpUhAd66yicgkBQWME54yxQSHePJgObeM2icPSdcWE2Trj15ByAdXVfQFkd4rRcbNCHtuabdFQDrqetU74AW0/640?wx_fmt=png&from=appmsg#imgIndex=17)

**3.3 方法三：预算思维**

在设计一个Loop时，不仅需要考虑技术实现，更需要考虑一个很现实的点： **预算**

预算收紧的今天，谁都不想，月初额度就用了一半！所以需要有一些策略应对：

**策略一：模型选择**

首先，预算思维的本质是： **资源倾斜 ，背后的问题是：什么样的任务我愿意投入更多的资源？**

针对高价值的任务，用聪明的模型，而针对低价值的重复任务，绝不用贵的模型。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr4NeSfKbqPoVLo81HhD7iaLR8mibCMBVCiaoiaD948aicXzqiao1YuhmspW5OgicicCpjUUQ3gX1KicxvbvEkofNM3W7zCjT1r71lHEgmwc/640?wx_fmt=png&from=appmsg#imgIndex=18)

选择不合适的模型，成本差距巨大，Opus的输出成本是GLM4-Flash的 **180倍** 。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr5Up1nomiaYm2QCE8JB3cSkPsYX3JFo91ibUy3yhpW0cWkbSpndAc2icGC8HnZTibtV1lZSH0G0JlicnhvDIng8vPnRicdcgZaibrOApw/640?wx_fmt=png&from=appmsg#imgIndex=19)

**策略二：设置退出机制**

设置退出机制就是针对每个任务要设置一个阈值上线，常见的有：

1. 最大的步骤限制
2. 预算熔断机制
![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr43KwDMatiaZdKT38HRBOcCax7UX86cRJtHPRJyJy6A2Q9T9qGDpA5ia4Av96N05s1Kk5Jt7KgGFp6pQ3cnatBkuqmUEGSBtzk3A/640?wx_fmt=png&from=appmsg#imgIndex=20)

**策略三：上下文压缩**

面对长周期 Agent 任务的成本问题，上下文压缩，是一个常见的方式，一般的做法是：用廉价模型对全量上下文反复重压缩，但这种操作，往往会 **实则会让核心规则持续稀释、过程噪音不断累积** 。最终导致任务跑偏、全链路已经投入的 Token 全部作废。

而这里我个人的一些应对思路是：高密度核心规则全程人为把控（不参与压缩）+增量信息克制压缩

把人的强判断力用在不可出错的核心约束上，把模型的压缩能力用在可损耗的过程信息上，从根源上避免压缩噪音污染核心逻辑。

## 04

写在最后

Loop不是一个技术框架，而是一种思维模式。让我们更好的去思考：人和AI如何协作完成一个Loop？把人从Loop中更多的环节拔出来，把注意力真正的还给人自己。

\-End-

原创作者｜吕昊俣

感谢你读到这里，不如关注一下？👇

![图片](https://mmbiz.qpic.cn/mmbiz_png/VY8SELNGe95UnhD9f7ia4T3ufXM1liaxxffiaEy41n0icohEC2qDS05icapaN4iaTVfsClibPRmqOjNW6q33PZicAVoSOg/640?wx_fmt=png&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=4)

你对本文内容有哪些看法？同意、反对、困惑的地方是？欢迎留言，我们将邀请作者针对性回复你的评论，欢迎评论留言补充。我们将选取1则优质的评论，送出腾讯云定制文件袋套装1个（见下图）。8月6日中午12点开奖。

![图片](https://mmbiz.qpic.cn/mmbiz_png/VY8SELNGe96Ad6VYX3tia1sGJkFMibI6902he72w3I4NqAf7H4Qx1zKv1zA4hGdpxicibSono28YAsjFbSalxRADBg/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=6)

扫码领取腾讯云开发者专属服务器代金券！

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr4nU3obq4B4URKhzJMmibw1uR1ZehOtyeel5hYevARgDqdKxqXvtzclLhu7g28g6PBib8M2uaQegic6MrCdBic0SdHh4XUQODQkmKk/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=16) ![图片](https://mmbiz.qpic.cn/mmbiz_png/VY8SELNGe95pIHzoPYoZUNPtqXgYG2leyAEPyBgtFj1bicKH2q8vBHl26kibm7XraVgicePtlYEiat23Y5uV7lcAIA/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=11)

腾讯技术人原创集 · 目录

同步

点击同步文章到多平台