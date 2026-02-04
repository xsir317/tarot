# 支付流程

## 概述

使用 Stripe 作为支付提供商，支持：

1. **按次付费**: $0.99 - $1.99 / 次
2. **包月订阅**: $9.99 / 月
3. **自愿打赏**: 用户满意后自愿打赏

## 按次付费流程

```
选择"按次付费" → 创建 Checkout Session → Stripe 支付
                                                       ↓
                                          payment_intent.succeeded Webhook
                                                       ↓
                                          创建支付记录 → 用户获得占卜资格
```

## 包月订阅流程

```
选择"包月订阅" → 创建 Checkout Session → Stripe 订阅
                                                       ↓
                                          subscription.created Webhook
                                                       ↓
                                          创建订阅记录 → 每日200次，每周700次
```

## Stripe Webhook 事件

| 事件类型 | 处理逻辑 |
|---------|---------|
| `payment_intent.succeeded` | 按次支付成功 |
| `customer.subscription.created` | 订阅创建 |
| `customer.subscription.deleted` | 订阅取消 |
| `invoice.payment_succeeded` | 订阅续费成功 |

## 环境变量

```bash
STRIPE_API_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://example.com
```
