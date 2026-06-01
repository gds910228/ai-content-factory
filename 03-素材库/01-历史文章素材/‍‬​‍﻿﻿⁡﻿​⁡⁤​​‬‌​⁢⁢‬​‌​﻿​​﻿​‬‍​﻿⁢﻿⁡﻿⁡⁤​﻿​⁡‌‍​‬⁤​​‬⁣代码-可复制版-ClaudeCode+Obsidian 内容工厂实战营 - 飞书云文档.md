---
title: "‍‬​‍﻿﻿⁡﻿​⁡⁤​​‬‌​⁢⁢‬​‌​﻿​​﻿​‬‍​﻿⁢﻿⁡﻿⁡⁤​﻿​⁡‌‍​‬⁤​​‬⁣代码-可复制版-ClaudeCode+Obsidian 内容工厂实战营 - 飞书云文档"
source: "https://yunyinghui.feishu.cn/wiki/L88DwT5DAihCDPk6gg7cb8kunxe?open_in_browser=true"
author:
published:
created: 2026-06-01
description:
tags:
  - "clippings"
---
输入“/”快速插入内容

// 1. 弹出输入框，让用户输入稿件标题

const 稿件标题 = await quickAddApi.inputPrompt("请输入稿件标题");

if (!稿件标题) {

new Notice("稿件标题不能为空！");

return;

}

// 2. 生成日期后缀，规范文件夹命名

const 日期 = moment().format("YYYYMMDD");

const 文件夹名称 = \`${稿件标题}-${日期}\`;

const 文件夹路径 = \`02-稿件库/01-创作中稿件/${文件夹名称}\`;

// 3. 创建稿件根文件夹和assets图片文件夹

try { await app.vault.createFolder(文件夹路径); } catch(e) {}

try { await app.vault.createFolder(\`${文件夹路径}/assets\`); } catch(e) {}

// 4. 读取访谈记录模板

let 访谈模板内容 = "";

const 模板文件 = app.vault.getAbstractFileByPath("00-模板库/模板-访谈记录.md");

if (模板文件) {

访谈模板内容 = await app.vault.read(模板文件);

访谈模板内容 = 访谈模板内容

.replace(/\\{\\{NAME\\}\\}/g, 稿件标题)

.replace(/\\{\\{DATE:YYYY-MM-DD\\}\\}/g, moment().format("YYYY-MM-DD"));

}

// 5. 创建所有笔记文件

const 文件列表 = \[

{ 文件名: "01-访谈记录.md", 内容: 访谈模板内容 },

{ 文件名: "02-初稿.md", 内容: \`# ${稿件标题} - 初稿\\n\\n\` },

{ 文件名: "03-改稿记录.md", 内容: \`# ${稿件标题} - 改稿记录\\n\\n\` },

{ 文件名: "04-定稿.md", 内容: \`# ${稿件标题} - 定稿\\n\\n\` }

\];

for (const 文件 of 文件列表) {

await app.vault.create(\`${文件夹路径}/${文件.文件名}\`, 文件.内容);

}

// 6. 弹出成功提示，打开访谈记录笔记

new Notice(\`稿件文件夹【${文件夹名称}】创建成功！\`);

const 目标笔记 = app.vault.getAbstractFileByPath(\`${文件夹路径}/01-访谈记录.md\`);

if (目标笔记) {

await app.workspace.getLeaf().openFile(目标笔记);

}

};

\---

kanban-plugin: basic

\---

\## 📌 选题池

\- \[ \] 在此处添加新选题，从「01-选题库」中挑选高优先级选题拖入

{-}

\## ✍️ 创作中

\- \[ \] 在此处添加正在创作的稿件，拖拽进入表示开始创作

{-}

\## 🔍 审核中

\- \[ \] 在此处添加等待审核/改稿的稿件

{-}

\- \[ \] 在此处添加已发布的稿件，记录发布日期和数据

{-}

评论（0）

跳转至首条评论

📞

Claude Code+Obsidian实战营课前准备 | GitHub等工具注册配置

💡

AI音乐变现实战营学习规则 | 7天掌握创作技巧

🧯

3个优化Claude Code DeepSeek API配置的实用技巧

🔎

为什么要在Obsidian中搭建知识库标准化架构？

🔍

Claude Skills实战营开营介绍 | 学习安排及群规说明

🖥️

安装章节相关命令行代码及环境变量设置教程

推荐内容由 AI 生成

真诚点赞，手留余香

0 字

- 上传日志

- 联系客服

- 功能更新

- 帮助中心

- 效率指南