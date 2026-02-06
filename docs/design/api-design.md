# API 设计文档

## 通用规范

- **Base URL**: `/api/v1`
- **Content-Type**: `application/json`
- **鉴权方式**: Bearer Token (JWT)
- **成功响应**:
  ```json
  {
    "success": true,
    "data": { ... }
  }
  ```
- **错误响应**:
  ```json
  {
    "success": false,
    "error": {
      "code": "ERROR_CODE",
      "message": "Human readable message",
      "details": { ... }
    }
  }
  ```

---

## 1. 认证 (Auth)

### 发送验证码
`POST /auth/send-code`

请求体：
```json
{
  "phone": "+1234567890", // 或 email
  "email": "user@example.com"
}
```

响应：
```json
{
  "code": "123456", // MVP阶段直接返回code用于测试
  "expires_in": 300
}
```

### 验证码登录/注册
`POST /auth/login/code`

请求体：
```json
{
  "phone": "+1234567890", // 或 email
  "code": "123456"
}
```

响应：
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "nickname": "User",
    "avatar": "url"
  }
}
```

### 刷新 Token
`POST /auth/token/refresh`

请求体：
```json
{
  "refresh_token": "eyJ..."
}
```

响应：
```json
{
  "access_token": "eyJ...",
  "expires_in": 900
}
```

---

## 2. 占卜 (Tarot)

### 验证问题
`POST /tarot/validate`

请求体：
```json
{
  "question": "我的事业运势如何？",
  "gender": "female", // 可选
  "language": "zh"
}
```

响应：
```json
{
  "suitable": true,
  "reason": "Suitable question",
  "redirect_message": null
}
```

### 抽牌 (Draw)
`POST /tarot/draw`

*无需参数，完全随机*

响应：
```json
{
  "cards": [
    {
      "id": "fool",
      "name_en": "The Fool",
      "name_zh": "愚者",
      "position": "upright", // upright/reversed
      "image_url": "/assets/cards/fool.jpg"
    },
    ...
  ]
}
```

### 解读 (Interpret)
`POST /tarot/interpret`

请求体：
```json
{
  "question": "我的事业运势如何？",
  "cards": [
    { "id": "fool", "position": "upright" },
    { "id": "magician", "position": "reversed" },
    { "id": "high_priestess", "position": "upright" }
  ],
  "language": "zh",
  "device_fingerprint": "optional_for_anonymous"
}
```

响应：
```json
{
  "reading_id": "uuid", // 保存后的记录ID
  "interpretations": [
    {
      "card_id": "fool",
      "text": "愚者代表..."
    },
    ...
  ],
  "overall_interpretation": "总体来看..."
}
```

---

## 3. 额度 (Quota)

### 获取额度
`GET /quota`

Query 参数：
- `device_fingerprint`: 匿名用户必填

响应：
```json
{
  "type": "anonymous", // anonymous, free_user, subscriber
  "remaining": 2,
  "total": 3,
  "reset_at": "2026-02-07T00:00:00Z"
}
```

---

## 4. 支付 (Payment)

### 创建 Checkout Session
`POST /payment/checkout`

请求体：
```json
{
  "product_type": "subscription", // subscription / one_time / tip
  "price_id": "price_H5ggY...", // Stripe Price ID (for subscription/fixed price)
  "amount": 500, // Optional: Amount in cents (for custom tip)
  "currency": "usd", // Optional: Default usd
  "reading_id": "uuid", // Optional: Associate payment with specific reading (for tips)
  "success_url": "https://tarot.com/result?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://tarot.com/pricing"
}
``````

响应：
```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/..."
}
```

### Webhook
`POST /payment/webhook`

*Stripe 标准 Webhook 格式*
