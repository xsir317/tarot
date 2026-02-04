# API 接口设计

## 基础信息
- 版本: v1.0
- 基础路径: `/api/v1`
- 协议: HTTPS
- 认证: JWT + HTTP-only Cookies

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "data": {},
  "message": "操作成功"
}
```

### 错误响应
`{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}
  }
}
```

---

## 认证相关 API

### POST /auth/register
注册新用户

**Request Body:**
```json
{
  "contact": "user@example.com",
  "code": "123456",
  "password": "securepassword",
  "nickname": "张三",
  "gender": "male"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "nickname": "张三",
    "free_quota": 3
  }
}
```

### POST /auth/login
用户登录

**Request Body:**
```json
{
  "contact": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "email": "user@example.com",
    "nickname": "张三"
  }
}
```

---

## 占卜相关 API

### POST /tarot/validate-question
验证问题是否适合占卜

**Request Body:**
```json
{
  "question": "我最近工作不顺，不知道该怎么办？",
  "gender": "male"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "suitable": true,
    "reason": "问题适合占卜",
    "redirect_message": null
  }
}
```

### POST /tarot/draw-cards
抽牌（不消耗额度）

**Request Body:**
```json
{
  "question": "我最近工作不顺，不知道该怎么办？",
  "gender": "male"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": "the_fool",
        "name": "愚者",
        "position": "upright",
        "image_url": "/cards/the_fool_upright.png",
        "keywords": ["新开始", "冒险", "天真"]
      }
    ]
  }
}
```

### POST /tarot/interpret
解读塔罗牌（消耗额度）

**Response (200):**
```json
{
  "success": true,
  "data": {
    "reading_id": "uuid",
    "individual_interpretations": [
      {
        "card_index": 0,
        "card_name": "愚者",
        "position": "upright",
        "interpretation": "愚者正位象征着新的开始..."
      }
    ],
    "overall_interpretation": "综合来看，这三张牌暗示...",
    "cards": []
  }
}
```

---

## 额度相关 API

### GET /quota
查询用户剩余额度

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user_type": "anonymous",
    "free_quota": {
      "remaining": 2,
      "total": 3,
      "reset_time": null
    },
    "subscription": null
  }
}
```

---

## 支付相关 API

### POST /payment/create-checkout-session
创建 Stripe Checkout 会话

**Request Body:**
```json
{
  "plan": "one_time",
  "amount": 990
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "checkout_url": "https://checkout.stripe.com/..."
  }
}
```

### POST /payment/webhook
Stripe Webhook 回调

---

## 错误代码

| 错误代码 | 描述 |
|---------|------|
| AUTH_001 | 验证码错误或已过期 |
| AUTH_002 | 用户已存在 |
| AUTH_005 | Token 无效或已过期 |
| QUOTA_001 | 免费额度已用完 |
| TAROT_001 | 问题不适合占卜 |
| PAYMENT_001 | 支付处理失败 |
