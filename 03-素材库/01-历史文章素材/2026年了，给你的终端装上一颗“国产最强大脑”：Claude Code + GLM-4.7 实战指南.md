---
title: "2026年了，给你的终端装上一颗“国产最强大脑”：Claude Code + GLM-4.7 实战指南"
source: "https://mp.weixin.qq.com/s/JrRrKGZFtBsQ7I5oAI_3Zw"
author:
  - "[[AI启蒙学习]]"
published:
created: 2026-06-04
description: "想拥有钢铁侠的Jarvis？3分钟搞定！用Claude Code（顶级AI框架）搭配GLM-4.7（国产高智商模型），你的笔记本秒变AI超级管家。通过简单配置，以超高性价比拥有这个“数字员工”，让你从重复劳动中解放，专注更有价值的事情。"
tags:
  - "clippings"
---
AI启蒙学习 *2026年1月5日 16:22*

你有没有幻想过《钢铁侠》里的 Jarvis？

你只需要说：“Jarvis，帮我查一下A股的收盘数据，分析出涨幅前三的板块，然后写一个Python脚本把这些数据可视化。”然后，你就可以去喝咖啡了，屏幕上代码自动飞舞，任务自动完成。

在 **Claude Code** 出现之前，这只是科幻电影。在 **GLM-4.7** 出现之前，实现这一点的成本高达每小时几十美金。

今天，我们要教你用 **Claude Code（目前体验最好的Agent框架）** 搭配 **GLM-4.7（国产高智商性价比之王）** ，在你的普通笔记本上，复刻一个平民版的 Jarvis。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Zn2lRwG7GeYIH5GuxnPtogwLtxQpgVjjjq22tlK1P8coSLDVciaEpKx6giaibia4Yys9QO4HSW65nspeia8B4qIGuWw/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

为什么要“移花接木”？

很多朋友会问：“Claude Code 不就是 Anthropic 公司的产品吗？为什么要用 GLM 的模型？”

这就好比 **“买车”** 和 **“换引擎”** 。

- **Claude Code (CC)** 是那辆 **法拉利的车身** 。它拥有极好的操控系统（CLI命令行），能直接操作你的电脑文件、运行终端命令。它是目前市面上体验最丝滑的系统级 Agent。
- **GLM-4.7** 则是智谱AI推出的 **国产核动力引擎** 。它的逻辑推理能力在2026年已经完全对标国际顶尖水平， **更懂中文语境** ，最关键的是—— **便宜** ！
	![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**我们要做的，就是把 GLM-4.7 这颗“强劲且省油”的心脏，装进 Claude Code 这辆“豪华超跑”里。**

保姆级实操——3分钟搭建你的AI员工

别被命令行吓到，跟着我做，只需要三步。

1. 安装车辆（Claude Code）

---

首先确保你的电脑有 Node.js 环境（没有去官网下个安装包就行）。

然后在终端输入：npm install -g @anthropic-ai/claude-code

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**能看到版本号即安装成功**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)
2. 更换引擎（配置 GLM 模型）

---

安装好后，我们需要把默认的 Claude 模型替换成 GLM，GLM官网接入Claude Code的配置文档：https://docs.bigmodel.cn/cn/guide/develop/claude

不过我自己的习惯是自己到C盘---用户---Administrator里头的.claude文件夹 ，手动建立一个setting.json配置文件。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

API Key可以从https://open.bigmodel.cn/ 的右上角控制台——右上角API Key，新建一个。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

json参数替换你的GLM api\_key即可。

```json
{  "env": {    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",    "ANTHROPIC_AUTH_TOKEN": "填写自己的APIKEY即可",    "API_TIMEOUT_MS": "3000000",    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",    "ANTHROPIC_MODEL": "glm-4.7-coding-preview",    "ANTHROPIC_SMALL_FAST_MODEL": "glm-4.7-coding-preview",    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7-coding-preview",    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-4.7-coding-preview",    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.7-coding-preview"  },  "enabledPlugins": {    "infopic@local-infopic-plugin": true  },  "alwaysThinkingEnabled": true}
```

然后你就可以在你的AI编程工具（我目前习惯了腾讯的CodeBuddy）的命令行里输入：claude，连上你的私人Jarvis

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

基础实战——让它帮你“算算运气”（彩票模拟器）

## 环境搭好了，它到底有多强？别整那些枯燥的代码了，我们来做一个很多人的梦想实验：“如果我每天花 10 块钱买彩票，坚持 10 年，我到底是会变成亿万富翁，还是血本无归？”

## 步骤 1：下达“白话”指令

我们在 `>>` 提示符后直接输入中文指令（注意，我们甚至不需要告诉它彩票规则，GLM-4.7 自己懂）：

> `>> 用 Python 写一个脚本，模拟“双色球”彩票。规则是：我每天花 10 元随机买 5 注，坚持 10 年。计算我的累计投入和累计中奖金额，最后画一张“盈亏走势图”保存在桌面。`

## 步骤 2：看着它“自动驾驶”

这时候，GLM-4.7 的大脑开始飞速运转，终端里会开始刷屏。请注意观察它是如何拆解任务的：

1. **思考与环境检查** ：它意识到需要画图，于是它 **自动执行** `pip install matplotlib` （如果你没装过的话）。
2. **逻辑构建** ：它会自动写出双色球的中奖规则（6红1蓝，一等奖概率等等）。
3. **代码生成与运行** ：它创建并运行了 `lottery_simulator.py` 。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 步骤 3：见证残酷的真相

几秒钟后，它提示任务完成。打开桌面上的图片，你可能会看到一条 **一路向下** 的残酷曲线。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 为什么要选这个例子？

1. **零门槛** ：不需要懂金融，不需要懂代码，只需要懂“钱”。
2. **成功率 100%** ：它只依赖 Python 基础库，不需要联网爬虫（爬虫容易被封），也不需要复杂的 API Key， **实操绝对不会翻车** 。
3. **Agent 能力体现** ：虽然是个小脚本，但体现了 Agent 的“逻辑拆解”（懂规则）、“环境管理”（装库）、“文件操作”（保存图片）全流程。

进阶魔法——MCP与Skills（给AI装上“三头六臂”）

如果说前面的操作只是让 AI 当个“码农”，那接下来的 **MCP (Model Context Protocol)** 和 Skills (技能)，才是真正让它进化成“超级管家”的关键。

**简单说：MCP 是给 AI 装上“义肢”连接外部世界，Skills 是给 AI 植入“肌肉记忆”让它学会独门绝招。**

一、MCP 实战：三行命令，打通“视、听、读”全能感官

以前你想让 AI 读个网页、看个视频，可能得来回复制链接。现在，我们要利用 GLM（智谱）官方提供的三个神器，直接在命令行里给 Claude Code 挂载“外挂”。

请在终端里依次执行以下三行命令（注意替换成你的 API Key）：

1. 挂载“千里眼”：联网搜索 (Web Search)

这就好比给 AI 拉了一根网线，让它不再是断网的傻瓜。

```sql
claude mcp add-s user-t http web-search-prime https://open.bigmodel.cn/api/mcp/web_search_prime/mcp --header "Authorization: Bearer 你的_GLM_API_KEY"
```

2. 挂载“显微镜”：深度网页阅读 (Web Reader)

搜索只能看概览，这个工具能让 AI 深入读取每一个网页的详细内容。

```nginx
claude mcp add -s user -t http web-reader https://open.bigmodel.cn/api/mcp/web_reader/mcp --header "Authorization: Bearer 你的_GLM_API_KEY"
```

3. 挂载“透视眼”：视频理解 (Video Understanding)

这是最炸裂的。给它一个 B 站或 YouTube 链接，它能直接“看”懂视频里讲了什么。

```nginx
claude mcp add -s user zai-mcp-server --env Z_AI_API_KEY=你的_GLM_API_KEY -- npx -y "@z_ai/mcp-server"
```

或者你可以直接修改配置文件，在C:\\Users\\Administrator\\.claude.json 进行配置。

```perl
"mcpServers": {  "web-search-prime": {    "type": "http",    "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",    "headers": {      "Authorization": "Bearer 你的_GLM_API_KEY"    }  },  "web-reader": {    "type": "http",    "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",    "headers": {      "Authorization": "Bearer 你的_GLM_API_KEY"    }  },  "zai-mcp-server": {    "type": "stdio",    "command": "npx",    "args": [      "-y",      "@z_ai/mcp-server"    ],    "env": {      "Z_AI_API_KEY": "你的_GLM_API_KEY",      "Z_AI_MODE": "ZHIPU"    }  }}
```

🔥 见证奇迹的时刻：一个指令调动所有工具

配置好后，我们来个高难度的。 **场景** ：我想学习 DeepSeek 最新的技术，但我不想自己读长文，也不想看半小时的视频。

**在终端输入指令：**

> `>> 请帮我搜索 DeepSeek 最新的技术架构分析，阅读一篇深度技术博客，同时观看这个相关的技术解读视频 [https://haokan.baidu.com/v?pd=wisenatural&vid=9905444489934965204]，最后综合这三方信息，给我写一份简短的技术总结。`

**GLM-4.7 的动作流（Chain of Thought）：**

1. **调用 Web Search** ：搜索“DeepSeek 架构分析”。
2. **调用 Web Reader** ：抓取并阅读搜索到的技术博客全文。
3. **调用 Video Tool** ：解析视频内容，提取关键帧信息。
4. **大脑融合** ：综合文字与视频信息，生成总结。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) ![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这就是cc自主调用MCP工具解决问题的能力。

**二、Skills 实战：一键“前端代码美容术”**

MCP 解决了“连接”问题， **Skills** 则解决“重复劳动”问题。你是不是经常需要对写好的代码进行优化？比如：检查无障碍性、规范 CSS 类名、优化图片加载。与其每次都啰嗦一大堆 Prompt，不如直接教它一个 **Skill（技能）** 。

1. 定义技能

安装就一句话指令的事，比如这个前端设计skills，对前端优化很有用。

```nginx
npx skills-installer install @anthropics/claude-code/frontend-design --client claude-code
```

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 然后我们可以告诉 Claude Code，给站点做前端UI的优化。
2. 实战演练

其实每次大模型更新我都会给自己的几个站点做优化，这次就拿cc的这个前端设计Skills做优化。想进一步深入学习MCP和Skills的同学，可以看看之前写的这篇文章 [Claude Skills 功能深度解析 | 从提示词工程到流程工程的革命性升级](https://mp.weixin.qq.com/s?__biz=MzkxMjYzMDM5NA==&mid=2247486550&idx=1&sn=02df80af9f55eca38377b6ceeb66bf6c&chksm=c108bb43f67f325570a66e32427cdb0736d0c38546511b9757c493407a860f9bcd3e37007909&token=771379540&lang=zh_CN&scene=21#wechat_redirect)

> `>> 使用frontend-design skill，优化当前站点`

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

<video src="https://mpvideo.qpic.cn/0bc3tmarsaabiqahalk2svuvdg6ddgnqcgia.f10002.mp4?dis_k=187d283cff4722c494f5953ba641e5e4&amp;dis_t=1780540908&amp;play_scene=10120&amp;auth_info=W8PqrZVyJnBWuITgnHNVSwd3OzkYFz5nSm97Zxg2LklnQxt3MkUcewMtflE5ERZyCGNt&amp;auth_key=21af3b5882140dc8403cc6c5e1142b04&amp;vid=wxv_4328627227631124492&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

终极福利——如何以“白菜价”拥有这套神装？

看到这里，你手里的工具已经极其强大了：

- **Claude Code** ：顶级的交互外壳（免费）。
- **GLM MCP** ：顶级的视觉听觉插件（配置免费）。
- **唯一的成本** ：GLM-4.7 的 API 算力消耗。

虽然 GLM-4.7 已经比国外的模型便宜很多，但在 Agent 模式下，因为它需要反复思考、调用工具、读取网页，Token 消耗是普通聊天的数倍。

**这里有一个只有内部玩家才知道的“省钱漏洞”：智谱的【拼好模】活动。**

官方为了推广 Agent 生态，推出了极其“不讲武德”的 **资源包套餐** 。

- **平时按量** ：跑完上面那套“视频+搜索”的复杂任务，可能需要十几块钱。
- **拼好模套餐** ：通过拼团订阅资源包，折算下来，相当于把价格打到了 **“地板价”** 。这就好比你去吃自助餐，原本单点一盘澳龙要 200，现在团购入场券只要 50 块，随便吃！

这是最适合新手低成本跑通 Agent 全流程的机会。用一杯咖啡钱，雇佣一个拥有“天眼”和“超级大脑”的私人助理，这笔账怎么算都划算。

👉 **\[扫码二维码直达“拼好模”活动专区\]**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

在 2026 年， **“会写代码”不再是核心竞争力，“会指挥 AI 写代码”才是。**

我们今天通过 **Claude Code + GLM-4.7 + MCP** ，其实是在搭建一个属于未来的工作流：人类只负责 **“定义意图”** （我要什么结果）， AI 负责 **“路径规划”** （用什么工具）， AI 负责 **“执行落地”** （写代码、看视频、改文件）。

赶紧按照上面的步骤，打开你的终端，输入第一行命令。相信我，当你看着屏幕上的光标自动跳动、任务自动完成的那一刻，你会感觉自己真的拥有了钢铁侠的 Jarvis。

等配置好你的私人Jarvis，第一个想连接的软件是什么？微信？飞书？还是你的股票账户？第一个想交给它的“懒人任务”是什么？（比如：每天自动监控特价机票？还是自动总结老板的视频会议？）

欢迎在评论区分享你的脑洞！

AI工具评测 · 目录

作者提示: 个人观点，仅供参考

继续滑动看下一个

AI启蒙学习

向上滑动看下一个