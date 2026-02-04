# 数据模型设计

## PostgreSQL 表结构

### users - 用户表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, NOT NULL | 用户 ID |
| email | VARCHAR(255) | UNIQUE, NULLABLE | 邮箱（与 phone 二选一） |
| phone | VARCHAR(20) | UNIQUE, NULLABLE | 手机号（与 email 二选一） |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt 加密后的密码 |
| nickname | VARCHAR(100) | NULLABLE | 用户昵称 |
| gender | VARCHAR(20) | NULLABLE | 性别: male/female/other/prefer_not_to_say |
| is_active | BOOLEAN | DEFAULT TRUE | 账号是否激活 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

---

### user_quotas - 用户免费额度表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, NOT NULL | 额度 ID |
| user_id | UUID | FK(users.id), NOT NULL | 用户 ID |
| remaining | INT | DEFAULT 3 | 剩余次数 |
| total | INT | DEFAULT 3 | 总次数 |
| week_start | DATE | NOT NULL | 本周起始日期（周一） |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

---

### anonymous_quotas - 匿名用户额度表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, NOT NULL | 记录 ID |
| device_fingerprint | VARCHAR(255) | NOT NULL | 设备指纹 |
| ip_address | VARCHAR(45) | NOT NULL | IP 地址 |
| remaining | INT | DEFAULT 3 | 剩余次数) |

---

### subscriptions - 订阅表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, NOT NULL | 订阅 ID |
| user_id | UUID | FK(users.id), NOT NULL | 用户 ID |
| stripe_subscription_id | VARCHAR(255) | UNIQUE, NOT NULL | Stripe 订阅 ID |
| plan | VARCHAR(20) | NOT NULL | 订阅计划: monthly |
| status | VARCHAR(20) | NOT NULL | 状态: active/canceled/past_due/expired |
| daily_limit | INT | DEFAULT 200 | 每日限制 |
| weekly_limit | INT | DEFAULT 700 | 每周限制 |
| current_period_start | TIMESTAMP | NULLABLE | 当前周期开始时间 |
| current_period_end | TIMESTAMP | NULLABLE | 当前周期结束时间 |
| cancel_at_period_end | BOOLEAN | DEFAULT FALSE | 周期结束后是否取消 |

---

### readings - 占卜记录表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, NOT NULL | 占卜 ID |
| user_id | UUID | FK(users.id), NULLABLE | 用户 ID（可为空，支持匿名用户） |
| question | TEXT | NOT NULL | 用户问题 |
| gender | VARCHAR(20) | NULLABLE | 用户性别 |
| language | VARCHAR(10) | NOT NULL, DEFAULT 'zh' | 语言 |
| cards | JSONB | NOT NULL | 抽到的牌（数组） |
| individual_interpretations | JSONB | NOT NULL | 逐张解读 |
| overall_interpretation | TEXT | NOT NULL | 整体解读 |
| quota_type | VARCHAR(20) | NOT NULL | 额度类型: free/subscription/one_time |

---

### one_time_payments - 一次性支付表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, NOT NULL | 支付 ID |
| user_id | UUID | FK(users.id), NULLABLE | 用户 ID（可为空） |
| stripe_payment_intent_id | VARCHAR(255) | UNIQUE, NOT NULL | Stripe Payment Intent ID |
| amount | INT | NOT NULL | 金额（分） |
| currency | VARCHAR(3) | DEFAULT 'usd' | 货币 |
| status | VARCHAR(20) | NOT NULL | 状态: pending/succeeded/canceled/failed |
| reading_id | UUID | FK(readings.id), NULLABLE | 关联的占卜记录 |

---

## Redis 数据结构

### 用户会会话
```
Key: session:{user_id}
Type: Hash
Fields:
  - device_id: string
  - device_info: JSON
  - last_active: timestamp
TTL: 7 days
```

### 匿名用户额度（临时）
```
Key: anonymous_quota:{device_fingerprint}
Type: Hash
Fields:
  - remaining: int
  - ip: string
TTL: 7 days
```

---

## 数据清理策略

| 表名 | 清理策略 | 清理周期 |
|------|---------|---------|
| anonymous_quotas | 删除过期记录 | 每天凌晨 |
| readings | 保留最近 6 个月 | 每周 |
