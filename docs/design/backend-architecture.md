# Backend Architecture

## Tech Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Async SQLAlchemy 2.0)
- **Cache**: Redis
- **Auth**: JWT (python-jose) + Bcrypt
- **LLM**: OpenAI SDK / Anthropic SDK
- **Payment**: Stripe SDK

## Directory Structure
```
backend/
├── app/
│   ├── api/          # API Endpoints
│   ├── core/         # Config, Database, Redis, Security
│   ├── models/       # SQLAlchemy Models
│   ├── schemas/      # Pydantic Schemas (Request/Response)
│   ├── services/     # Business Logic (Auth, Tarot, Payment)
│   └── utils/        # Helpers
├── tests/            # Pytest Suite
└── alembic/          # Database Migrations
```

## Key Components

### 1. Authentication Strategy
- **Token Based**: Access Token (15 min) + Refresh Token (7 days).
- **Verification Code**: Stored in Redis with 5 min TTL.
- **Passwordless**: Primary login method via Phone/Email code.

### 2. LLM Integration
- **Service Layer**: `LLMService` handles prompt engineering and API calls.
- **Prompting**:
  - Validation Prompt: JSON output, strict safety filters.
  - Interpretation Prompt: Warm, supportive tone, JSON output.
- **Fallback**: Graceful error handling if LLM API fails.

### 3. Payment Flow (Stripe)
- **Checkout**: Server-side session creation.
- **Webhook**: Async processing of payment events (`payment_intent.succeeded`, `invoice.payment_succeeded`).
- **Idempotency**: Webhook handling must be idempotent.

### 4. Quota System
- **Anonymous**: Tracked via `device_fingerprint` (Redis/DB).
- **Registered**: Tracked via `user_quotas` table.
- **Reset**: Weekly reset logic (Cron job or Lazy check).
