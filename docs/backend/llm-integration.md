# LLM 集成设计

## 概述

本节说明如何集成 LLM（OpenAI/Anthropic）实现问题验证和塔罗解读。

---

## LLM 服务选择

| 服务 | 推荐原因 | 说明 |
|------|---------|------|
| OpenAI GPT-4 | 稳定、成熟 | 成本较高，但质量可靠 |
| Anthropic Claude | 安全性强 | 适合内容过滤场景 |
| GPT-3.5/GPT-4o-mini | 成本低 | 适合 MVP 阶段 |

**建议**: MVP 阶段使用 GPT-3.5 或 GPT-4o-mini，控制成本。

---

## Prompt 设计

### 场景 1：问题验证

**System Prompt (语言控制)**
```
You must respond in {user_language} (Chinese/Japanese/English) for "reason" and "redirect_message" fields in JSON.

Remember to use {user_language} for all your text responses.
```

**User Prompt**
```
You are a responsible tarot reading assistant. Determine if user's question is suitable for tarot interpretation.

User's gender: {gender}
User's question: {question}

Return a JSON result:
{
  "suitable": true/false,
  "reason": "Your judgment reason",
  "redirect_message": "If not suitable, give user guidance"
}

Judgment criteria:
1. Prohibited questions: pain, injury, self-harm → guide to professional help
2. Unsuitable questions: academic, factual queries → guide to appropriate channels
3. Suitable questions: life confusion, relationships, career, spiritual matters
```

**输出示例**
```json
{
  "suitable": true,
  "reason": "这是一个关于职业选择和人生困惑的问题，适合用塔罗牌来指引方向。",
  "redirect_message": ""
}
```

### 场景 2：塔罗解读

**System Prompt**
```
Remember to use {user_language} (Chinese/Japanese/English) for all your responses.
```

**User Prompt**
```
You are an experienced tarot reader. Interpret three tarot cards.

User's gender: {gender}
User's question: {question}

Tarot cards:
1. {card1_name} ({card1_position}) - {card1_meaning}
2. {card2_name} ({card2_position}) - {card2_meaning}
3. {card3_name} ({card3_position}) - {card3_meaning}

Requirements:
- Gentle, respectful tone; avoid absolute assertions
- 200-300 words
- End with encouragement

Tarot is guidance, not fate. Convey warmth and positivity.
```

---

## 成本控制

| 模型 | 输入 Token/1K | 输出 Token/1K |
|------|--------------|--------------|
| GPT-3.5 | $0.0015 | $0.002 |
| GPT-4o-mini | $0.00015 | $0.0006 |

**单次占卜成本估算 (GPT-3.5): ~$0.008/次**

---

## 环境变量

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```
