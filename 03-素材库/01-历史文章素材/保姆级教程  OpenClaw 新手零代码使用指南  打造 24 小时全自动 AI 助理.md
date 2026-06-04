---
title: "保姆级教程 | OpenClaw 新手零代码使用指南 | 打造 24 小时全自动 AI 助理"
source: "https://mp.weixin.qq.com/s/f2yIxlefVgIPdbc9fpEZkQ"
author:
  - "[[艾启蒙]]"
published:
created: 2026-06-04
description: "最近 AI 圈的 OpenClaw（龙虾）彻底火出圈了！但面对复杂的命令行，技术小白该如何跨越代码高墙？"
tags:
  - "clippings"
---
艾启蒙 *2026年3月3日 21:05*

导读： 最近 AI 圈的 OpenClaw（龙虾）彻底火出圈了！但面对复杂的命令行，技术小白该如何跨越代码高墙？本文将带你零代码解锁这款目前最强的本地 AI Agent，不仅保留了原汁原味的“养虾”避坑经验，还附送手把手的飞书机器人自动化接入教程。准备好解放双手，领养你的专属 AI 助理了吗？

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/POXYnuKicKs3VB5qlsMdpPYkJqrPuD7XYIGFGvf7026T5OvN4vLEfSggm7qhyrFziccyjYiaaXzP9aLjzibgt4LmXpZtYytgib7l33qtBQDX7KWs/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

## 现象级爆款：为什么到处都是“逮虾户”？

最近，AI 圈的一个新产品火出圈了——OpenClaw（圈内戏称“龙虾”，即之前改名的 Clawbot 开源项目）。我去看了眼 Github，Star 数已经飙升到 240K，这绝对是今年最具人气的开源 AI 项目，简直太🐂🍺了！

到处都是“逮虾户”在晒自己的龙虾。火到什么程度？连我那些平时只关心选品和股价波动的电商群、美股群，都开始热烈讨论怎么安装 OpenClaw 了。

OpenClaw 到底是什么？ 它是一个个人自主型本地 AI Agent。如果说 ChatGPT、豆包、元宝是“嘴强王者”（只给云端建议，不知道现实世界发生了什么），那么 OpenClaw 就称得上是“动手实干家”（在你的世界中行动，实时感知真实结果）。它具备以下颠覆性特点：

1. 1\. 自我迭代：能自己写程序或使用互联网工具，不断试错实现你的需求。
2. 2\. 操作本地：可以直接读取和操作你电脑里的本地文件。
3. 3\. 长期记忆：记住你的工作习惯和偏好，下次直接执行，无需反复调教。
4. 4\. 自主决策：实现多步骤任务自动化。比如你说“帮我整理上周销售数据并发邮件给老板”，它会自动拆解为：找文件 → 清洗数据 → 生成图表 → 写邮件 → 发送。

痛点来了：小白的“代码高墙” 正因为 OpenClaw 有真实的“手”，存在安全风险，官方教程默认你熟悉命令行、会用 AI 编程工具。这对非技术人员来说是一道高墙。更要命的是它稳定性欠佳，经常改错配置文件导致服务挂掉。我帮几个好友在云端部署后，硬生生把自己逼成了 AI 时代的“网管”，每天都要去“救活”死掉的龙虾。

---

## 破局工具：最适合小白的 LobsterAI

如果真的想吃螃蟹，到底如何才能最简单地体验 OpenClaw 的魅力？答案是：LobsterAI（有道龙虾）。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这是网易有道刚开源的桌面级 Agent，一个 7x24 小时运行的全场景个人助理。它不仅完美继承了 OpenClaw 的能力，还在易用性和安全性上做了极大提升（优点）：

- 开箱即用：提供安装包，本地运行，UI 界面可视化配置所有参数，彻底告别命令行。
- 多模型支持：支持国内外各家 LLM，聊天界面就像 ChatGPT 一样亲切。
- 生态打通：在 UI 里点几下，就能打通飞书、钉钉、Telegram、Discord，还能读取并发送邮件。
- 技能扩展：内置网页搜索，支持按需手动安装各类 Skills。
- 极致安全：类似 Claude Cowork，支持设置“仅沙箱运行”，极大保护你的本地数据安全。

下载地址：https://lobsterai.youdao.com/

使用手册：https://lobsterai.youdao.com/#/docs/lobsterai\_user\_manual

Github: https://github.com/netease-youdao/LobsterAI

我给有道龙虾配置的是智谱的模型，可以买一个 Coding Plan，一个月的成本大概在 46 块。跟 MiniMax 和 Kimi 价格相当。众所周知龙虾最吃 token，开一个包月是非常划算的。

https://www.bigmodel.cn/glm-coding?ic=XXUE25NZRU

然后可以来到 LobsterAI 进行配置。

💡 成本实测提示（缺点规避）： 众所周知，OpenClaw 这种自动规划任务的 Agent 最吃 Token。我给有道龙虾配置的是智谱 GLM 模型，买一个 Coding Plan，一个月的成本大概在 46 块（与 Kimi 和 MiniMax 价格相当），开包月跑自动化是最划算的。

---

## 我的“养虾”故事：OpenClaw 到底能干什么？

我大概从 1 月 26 日 OpenClaw 还没火出圈时就开始玩，踩了不少坑。大家最常问的问题一定是：它到底能帮我干什么？

其实，我把它形容为成年人的“乐高”，理论上，只要是你在电脑上手动能做的重复性操作，它都可以帮你自动化实现。

刚装上时我特别兴奋，但玩了两天却觉得索然无味，感觉不出它比 Claude Code 强在哪。后来我才意识到：养虾第一件事，是先找到真正的使用场景。 对比常规代码助手，OpenClaw 的核心优势在于随时随地的 IM 交互和主动触发的定时任务。

我的破局场景：飞书全自动 AI 资讯助理

- 困境：我每天早上都需要花大量时间浏览各大科技网站，汇总 AI 圈的最新资讯，十分耗时。
- 解决过程：我把 LobsterAI 连上了飞书。我把抓取新闻的工作流封装成了龙虾里的一个“Skill（技能）”，并设置了定时任务。
- 成果展示：现在，每天早上 8 点，我的飞书群会准时收到一份排版精美的 AI 日报，涵盖知乎、36 氪、机器之心等各大平台。我每天只需要在地铁上划划手指，就能获取最前沿的消息。

---

## 手把手教程：如何让 LobsterAI 接入飞书？

为了让你也能跑通上述的“每日早报”任务，我将原本复杂的飞书机器人接入过程梳理成了以下结构化的步骤：

### 在飞书开放平台创建应用

需要使用您的飞书账号登录 https://open.feishu.cn/app。登录成功后，点击创建企业自建应用。

填写应用名称（如 “OpenClaw 助手”）、应用描述，选择应用图标，点击创建按钮，进入应用管理页面。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 添加机器人

在前一步所创建应用的管理页面，左侧导航栏中找到并点击添加应用能力，在弹出的列表中选择机器人，点击添加。

### 发布应用

1. 1\. 左侧菜单 →「版本管理与发布」
2. 2\. 点击「创建版本」→ 填写版本号（如 1.0.0）→ 提交
3. 3\. 等管理员审批通过（如果你就是管理员，直接通过）

### 查询 AppID 和 AppSecret

在左侧导航栏找到 “凭据与基础信息” ，点击进入。在页面中找到 “App ID” 和 “App Secret” 两个参数，分别点击右侧 “复制” 按钮，将其保存到个人记事本或备忘录中（注意数据安全，勿泄露），后续步骤中需要使用。

### 为 OpenClaw 配置 IM 通道

接下来需要为 OpenClaw 配置 IM 机器人通道，选飞书。

### 飞书机器人相关配置

#### 事件配置

在飞书应用管理页，左侧导航栏找到 “事件与回调” ，点击进入页面。在“事件配置”页签中选择 “长连接接收事件”，点击保存。

⚠️注意：如果这一步报错提示“应用未建立长连接”，请检查前面步骤中的机器人 App ID 和 App Secret 是否已正确配置。

此时如果事件配置保存成功，可直接前往后续的“添加事件”步骤。

#### 添加事件

点击“事件配置”页面中的 “添加事件”，在弹出的列表中，搜索并添加 “接收消息”，点击 “确认添加”，按照指引确认开通权限。

（推荐）若期望将飞书机器人添加进聊天群组中使用，可以参考前述步骤继续添加更多群组相关权限，主要包括“消息已读”、“机器人进群”、“机器人被移出群”。否则，请跳过本步骤。

#### 回调配置

在“事件与回调-回调配置”页面中，订阅方式选择 “使用长连接接收回调”，点击保存，无需填写其他地址，配置自动生效。

#### 权限配置

在飞书应用管理页，左侧导航栏找到 “权限管理” ，点击进入页面。点击页面中的 “批量导入权限” 按钮，弹出权限导入窗口。

复制以下代码，替换前面弹窗中原有的 JSON 内容，点击下一步，确认新增权限，继续申请开通，确认后等待权限导入完成。

```
{    "scopes": {
        "tenant": [
          "aily:file:read",
          "aily:file:write",
          "application:application.app_message_stats.overview:readonly",
          "application:application:self_manage",
          "application:bot.menu:write",
          "cardkit:card:write",
          "contact:contact.base:readonly",
          "contact:user.employee_id:readonly",
          "corehr:file:download",
          "docs:document.content:read",
          "event:ip_list",
          "im:chat",
          "im:chat.access_event.bot_p2p_chat:read",
          "im:chat.members:bot_access",
          "im:chat:readonly",
          "im:message",
          "im:message.group_at_msg:readonly",
          "im:message.group_msg",
          "im:message.p2p_msg:readonly",
          "im:message:readonly",
          "im:message:send_as_bot",
          "im:resource",
          "sheets:spreadsheet",
          "wiki:wiki:readonly"
        ],
        "user": [
          "aily:file:read",
          "aily:file:write",
          "contact:contact.base:readonly",
          "im:chat.access_event.bot_p2p_chat:read"
        ]
      }
    }
```

到这里，飞书相关配置告一段落，继续创建新的版本并发布

在飞书应用管理页，左侧导航栏找到 “版本管理与发布” ，点击进入页面。点击右上角的创建版本。

### 与飞书机器人进行交互

完成前面的步骤之后，您可以与飞书机器人进行单独聊天，或者将飞书机器人添加进群聊。

单独聊天

以电脑版飞书软件为例（手机端飞书的操作类似），登录飞书后，点击创建群组，然后点击设置——群机器人——添加群机器人。

然后在 LobsterAI 新建任务，就是本地建一个项目文件夹，TestDaily。

接下来可以群里@机器人，至此 OpenClaw 和飞书的交互就搞定啦。

过程可以在 LobsterAI 的 IM 机器人进行通联性测试。

好，接下来我们先来一个简单的对话任务。

### 创建自己的定时任务 Skills

> 提示词：
> 
> 帮我汇总今天最新的 AI 日报，在你的信息源里，增加以下渠道： 1、知乎 AI 热榜 2、36 氪 3、机器之心 4、量子位 5、MIT Technology Review 6、arXiv.org

当我们觉得内容质量达标后，直接让它把这套流程写成 skill，并在每天早上 8 点推送给我。

> 提示词：
> 
> 根据前面聊的内容，把这个 AI 日报沉淀成一个 Skills 保存起来，然后设置一个定时任务：
> 
> 1.每天早上 8:00 准时给我推送到飞书群；
> 
> 2.准时执行这个日报 Skills，为我推荐并列举当天的 AI 日报新闻；

---

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 避坑与思考

给所有想尝试 自动化工具 的新手的两点核心建议：

1. 1\. 先用成品，别死磕源码：新手尽量使用 LobsterAI、Clawdy、Kimi Claw 这类已经封装好的开箱即用产品。不要一上来就尝试原版本地部署，很容易陷入“一直在查 Bug，却从未真正开始养虾”的死循环。
2. 2\. 工具是表象，流程是核心：AI 时代技能是学不完的，今天火 Cursor，明天火 OpenClaw，后天又有新 Agent。与其盲目追逐新工具，不如围绕自己的高频工作场景做深。想清楚“龙虾到底用来做什么”，把你日常的标准化流程梳理出来，才是真正能沉淀下来的护城河。

---

💬 评论区聊聊： 如果现在给你配置好了一个 24 小时待命的 OpenClaw 助手，你最想把工作中哪项“枯燥、重复、耗时”的任务完全丢给它去自动完成？

保姆级教程 · 目录

作者提示: 个人观点，仅供参考

继续滑动看下一个

AI启蒙学习

向上滑动看下一个