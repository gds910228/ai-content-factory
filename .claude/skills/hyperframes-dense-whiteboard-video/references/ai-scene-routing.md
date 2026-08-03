# AI 文章识别与镜头路由

在生成 storyboard 前读取文章全文并填写 `contentProfile`。不要仅做关键词匹配；判断 AI 是否是文章主旨、概念是否形成技术关系、段落是在解释原理还是只提到工具名称。

## 领域识别

计算 `aiConfidence`（0～1），综合考虑：

- 核心问题是否在解释 AI 模型、方法、系统或产品。
- AI 概念是否贯穿标题、开头、主体和结论。
- 是否存在输入、数据、模型、工具、输出、评测等技术关系。
- 删除 AI 相关段落后，文章主旨是否仍然成立。
- AI 是技术对象，还是写作、效率或行业观点中的背景工具。

路由规则固定为：

- `aiConfidence >= 0.72`：`resolvedDomainPreset: ai-explainer`
- `0.45 <= aiConfidence < 0.72`：`resolvedDomainPreset: hybrid`
- `aiConfidence < 0.45`：`resolvedDomainPreset: general`

`general` 不套用 AI 图标。`hybrid` 只为被明确识别的 AI 概念使用视觉词典，其余镜头保持通用表达。

## 内容画像

- `domain`：`ai`、`mixed` 或 `general`。
- `topics`：只写文章实际涉及的具体概念，例如 `RAG`、`Agent`、`API`。
- `technicalDepth`：`beginner`、`intermediate` 或 `advanced`。
- `audience`：用简短中文描述。
- `articleType`：概念解释、工作流、对比、教程、观点、新闻、案例或混合。
- `signals`：列出支持判断的 2～6 个语义信号。
- `reason`：用一句话解释为何选择该预设。

最小示例：

```json
{
  "contentProfile": {
    "domain": "ai",
    "aiConfidence": 0.93,
    "resolvedDomainPreset": "ai-explainer",
    "topics": ["RAG", "向量检索"],
    "technicalDepth": "beginner",
    "audience": "刚接触大模型应用的普通读者",
    "articleType": "workflow",
    "signals": ["全文核心问题是 RAG 如何工作", "主体包含检索、资料和模型之间的数据流"],
    "reason": "文章以 RAG 技术流程为主旨。"
  },
  "project": {
    "visualStyle": "dense-whiteboard",
    "domainPreset": "auto"
  }
}
```

## 镜头模板

| visualPattern | 适用文案 | 默认结构 |
|---|---|---|
| `pipeline` | 怎么工作、步骤、数据流 | 输入→处理→输出 |
| `architecture` | 由哪些模块组成、系统结构 | 中央系统＋内部/外部模块 |
| `comparison` | A 与 B 的区别、方案选择 | 左右两列＋共同评价维度 |
| `loop` | Agent、反馈、自我修正 | 目标→行动→观察→循环 |
| `cause-effect` | 为什么、风险来源、机制 | 原因→机制→结果/对策 |
| `timeline` | 演进、训练阶段、历史 | 从左到右的阶段链 |
| `hub-spoke` | 一个核心分成多个能力 | 中心节点＋3～5 个分支 |
| `metric-dashboard` | 成本、速度、质量、评测 | 主结果＋2～4 个指标 |
| `general` | 不属于上述结构 | 使用通用知识白板布局 |

每个镜头选择一个主模板。不要因为同一段出现多个技术词，就混合两套互相竞争的版式。

## 路由示例

- “RAG 如何减少无依据回答”→ `pipeline`，概念顺序为问题、检索、资料、模型、回答。
- “Agent 如何完成复杂任务”→ `loop`，概念顺序为目标、规划、工具、观察、记忆。
- “提示词、RAG 与微调的区别”→ `comparison`，统一比较知识来源、成本和适用场景。
- “为什么模型会产生幻觉”→ `cause-effect`，显示信息缺口、概率生成、错误答案与核查。
- “API 调用为什么有延迟”→ `pipeline` 或 `metric-dashboard`，显示请求、排队、推理、响应和耗时。
