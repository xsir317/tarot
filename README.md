## 项目概览

塔罗牌占卜工具 MVP - 一个提供在线塔罗占卜服务的 Web 应用。

核心流程：
1. 用户输入问题 → LLM 判断是否适合占卜
2. 随机抽取 3 张塔罗牌（带洗牌、抽牌动画）
3. 用户依次翻牌，展示逐张解读
4. 展示整体解读，支持再次占卜

关键特性：
- 问题过滤（病痛/自伤引导就医，无意义问题礼貌拒绝）
- 免费额度策略（未登录 3 次，已登录每周 3 次）
- 付费方式（按次 0.99-1.99 美元、包月 9.99 美元/月、）
- 多语言支持（中英文）
- 历史记录（保留 6 个月）

## 技术栈

### 前端
- Next.js 14+ (App Router)
- shadcn/ui 或 Chakra UI（UI 组件）
- Framer Motion（动画：洗牌、翻牌效果）
- Zustand 或 React Context（状态管理）
- React Hook Form + Zod（表单验证）
- next-intl（国际化）

### 后端
- Python 3.11+
- FastAPI（Web 框架）
- OpenAI SDK 或 Anthropic SDK（LLM 集成）
- SQLAlchemy 2.0（ORM，异步）
- Alembic（数据库迁移）
- Pydantic（数据验证）
- python-jose（JWT）
- bcrypt（密码加密）

### 数据库 & 缓存
- PostgreSQL（主数据库）
- Redis（缓存、会话）

### 部署
- Docker + Docker Compose
- Nginx（反向代理）
- Let's Encrypt / Certbot（SSL）

### 支付
- Stripe（海外市场）
  - 支持订阅、一次性付款、
  - Webhooks 处理支付状态

### 认证
- JWT + HTTP-only Cookies
  - Access token + Refresh token

### 邮件/短信
- 邮件：SendGrid / AWS SES / Resend
- 短信：Twilio

## 文档结构

```
docs/
├── product/
│   ├── mvp-vision.md          # 产品愿景和核心流程
│   ├── user-flow.md           # 详细用户流程图
│   └── prd.md                 # 产品需求文档
│
├── design/
│   ├── api-design.md          # API 接口设计
│   ├── data-model.md          # 数据模型设计（表结构）
│   └── state-flow.md          # 状态流转图
│
├── frontend/
│   ├── pages-flow.md          # 页面跳转逻辑
│   ├── component-design.md    # 组件设计
│   └── animation-spec.md      # 动画设计规范
│
└── backend/
    ├── auth-strategy.md       # 认证策略
    ├── payment-flow.md        # 支付流程
    ├── quota-strategy.md      # 额度策略
    └── llm-integration.md     # LLM 集成
```

## 开发约定

### LLM Prompt 语言策略
- **Prompt 全部使用英文编写**，避免维护多份语言版本
- 在 system prompt 中强制使用用户语言：
  - 开头：`You must respond in {user_language}.`
  - 结尾：`Remember to use {user_language} for all your responses.`
- 用户语言：自动检测或用户手动选择（支持 Chinese / Japanese / English）

### 代码风格
- Python: Ruff（lint + format）
- JavaScript/TypeScript: ESLint + Prettier
- Pre-commit hooks：自动格式化

### Git 提交消息格式
```
[type] subject

body

footer
```

类型：feat, fix, docs, style, refactor, test, chore

### 分支策略
- `main`: 生产环境
- `develop`: 开发环境
- `feature/*`: 功能分支

## 开发工作流程

（重要）本项目采用严格的 TDD（测试驱动开发），所有新增或修改功能都必须遵循 **红-绿-重构** 循环。

详细规范请参考：**`docs/tdd-workflow.md`**

---

## 重要文件路径

| 文件 | 路径 |
|------|------|
| 开发工作流程 | docs/development-workflow.md |
| TDD 工作流程 | docs/tdd-workflow.md |
| 产品愿景 | docs/product/mvp-vision.md |
| 产品需求 | docs/product/prd.md |
| API 设计 | docs/design/api-design.md |
| 数据模型 | docs/design/data-model.md |
| 用户流程 | docs/product/user-flow.md |
| 认证策略 | docs/backend/auth-strategy.md |
| 支付流程 | docs/backend/payment-flow.md |
| 额度策略 | docs/backend/quota-strategy.md |
| LLM 集成 | docs/backend/llm-integration.md |
| 页面跳转 | docs/frontend/pages-flow.md |
| 组件设计 | docs/frontend/component-design.md |
| 动画规范 | docs/frontend/animation-spec.md |
| 部署与运维指南 | docs/deployment-and-operations.md |

## 部署架构

```yaml
# docker-compose.yml 主要服务
services:
  frontend:     # Next.js
  backend:      # FastAPI
  postgres:     # PostgreSQL
  redis:        # Redis
  nginx:        # Nginx
  certbot:      # SSL 证书
```

## 注意事项

### 成本控制
- Prompt 优化：控制输出长度
- 流式响应：改善用户体验
- LLM 成本监控：必要时记录 token 使用量

### 安全
- 敏感信息使用环境变量管理
- JWT 有效期合理设置
- HTTP-only Cookies 防止 XSS
- 输入验证和过滤

### 额度策略
- 未登录：设备指纹 + IP + localStorage 组合
- 已登录：基于用户 ID
- 包月限制：每天 200 次，每周 700 次
