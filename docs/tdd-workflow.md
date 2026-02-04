# TDD 工作流程规范

## 概述

本项目采用严格的 TDD（测试驱动开发）方法。所有新增或修改的功能都必须遵循 **红-绿-重构** 循环。

## 红绿重构循环

### 第一步：红色（Red）- 编写失败的测试

在编写任何生产代码之前，先编写一个失败的测试。

#### 原则
- **不通过测试绝不写生产代码**
- 测试应该清晰地表达期望的行为
- 测试名应描述被测试的行为

#### 后端示例（FastAPI + pytest）

```python
# tests/test_quota.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_anonymous_user_has_3_free_quota():
    """测试未登录用户有 3 次免费额度"""
    response = client.get("/api/quota")
    assert response.status_code == 200
    assert response.json()["remaining"] == 3
```

#### 前端示例（Next.js + Jest/Vitest）

```typescript
// __tests__/hooks/useQuota.test.ts

import { renderHook, act } from '@testing-library/react'
import { useQuota } from '@/hooks/useQuota'

describe('useQuota', () => {
  it('should return 3 remaining quota for anonymous user', () => {
    const { result } = renderHook(() => useQuota())
    expect(result.current.remaining).toBe(3)
  })
})
```

#### 运行测试确认失败

```bash
# 后端
pytest tests/test_quota.py -v  # 应该看到 FAILED

# 前端
npm test -- useQuota  # 应该看到 FAIL
```

---

### 第二步：绿色（Green）- 编写最简代码使测试通过

编写**刚好足够**让测试通过的生产代码，不要过度设计。

#### 原则
- **只写能通过测试的最少代码**
- 可以写"丑陋"的代码（硬编码、重复等），重构阶段再优化
- 不要提前优化

#### 后端示例

```python
# src/api/quota.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/quota")
async def get_quota():
    return {"remaining": 3}  # 最简实现，硬编码
```

#### 前端示例

```typescript
// src/hooks/useQuota.ts

import { useState } from 'react'

export function useQuota() {
  return { remaining: 3 }  // 最简实现
}
```

#### 运行测试确认通过

```bash
# 后端
pytest tests/test_quota.py -v  # 应该看到 PASSED

# 前端
npm test -- useQuota  # 应该看到 PASS
```

---

### 第三步：重构（Refactor）- 优化代码

在测试保护下，优化代码结构和质量，同时保持测试通过。

#### 原则
- **重构时必须保持测试通过**
- 提取重复代码
- 改善命名
- 应用设计模式

#### 后端示例

```python
# src/api/quota.py

from fastapi import APIRouter, Depends
from src.services.quota_service import QuotaService

router = APIRouter()

@router.get("/quota")
async def get_quota(quota_service: QuotaService = Depends()):
    remaining = await quota_service.get_anonymous_quota()
    return {"remaining": remaining}
```

```python
# src/services/quota_service.py

class QuotaService:
    ANONYMOUS_FREE_QUOTA = 3

    async def get_anonymous_quota(self) -> int:
        return self.ANONYMOUS_FREE_QUOTA
```

#### 前端示例

```typescript
// src/services/quota.ts

const ANONYMOUS_FREE_QUOTA = 3

export async function getAnonymousQuota(): Promise<number> {
  return ANONYMOUS_FREE_QUOTA
}
```

```typescript
// src/hooks/useQuota.ts

import { useState, useEffect } from 'react'
import { getAnonymousQuota } from '@/services/quota'

export function useQuota() {
  const [remaining, setRemaining] = useState<number>(0)

  useEffect(() => {
    getAnonymousQuota().then(setRemaining)
  }, [])

  return { remaining }
}
```

#### 运行测试确认依然通过

```bash
# 后端
pytest tests/test_quota.py -v  # 应该依然看到 PASSED

# 前端
npm test -- useQuota  # 应该依然看到 PASS
```

---

## 完整工作流程示例

### 场景：实现"用户额度检查"功能

#### 1. 红色阶段

```python
# tests/test_quota_service.py

def test_decrement_quota_reduces_remaining():
    """测试扣减额度会减少剩余次数"""
    service = QuotaService()
    service.set_quota(user_id="123", remaining=5)

    service.decrement(user_id="123")

    assert service.get_quota(user_id="123").remaining == 4
```

```bash
pytest tests/test_quota_service.py -v
# FAILED - QuotaService.set_quota not defined
```

#### 2. 绿色阶段

```python
# src/services/quota_service.py

class QuotaService:
    def set_quota(self, user_id: str, remaining: int):
        pass  # 最简实现

    def decrement(self, user_id: str):
        pass  # 最简实现

    def get_quota(self, user_id: str):
        return {"remaining": 4}  # 硬编码通过测试
```

```bash
pytest tests/test_quota_service.py -v
# PASSED
```

#### 3. 重构阶段

```python
# src/services/quota_service.py

from typing import Dict

class QuotaService:
    def __init__(self):
        self._quotas: Dict[str, int] = {}

    def set_quota(self, user_id: str, remaining: int):
        self._quotas[user_id] = remaining

    def decrement(self, user_id: str):
        if user_id in self._quotas:
            self._quotas[user_id] -= 1

    def get_quota(self, user_id: str) -> Dict[str, int]:
        remaining = self._quotas.get(user_id, 0)
        return {"remaining": remaining}
```

```bash
pytest tests/test_quota_service.py -v
# PASSED - 重构后依然通过
```

---

## 本项目的测试工具配置

### 后端测试配置

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
```

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    yield TestClient(app)

@pytest.fixture
def db_session():
    # 测试数据库 session
    ...

@pytest.fixture(autouse=True=True)
def cleanup_db(db_session):
    # 每个测试后清理
    yield
    db_session.rollback()
```

### 前端测试配置

```json
// vitest.config.ts
{
  "test": {
    "include": ["**/__tests__/**/*.ts", "**/*.test.ts"],
    "coverage": {
      "provider": "v8",
      "reporter": ["text", "html"]
    }
  }
}
```

---

## TDD 最佳实践

### 1. 单元测试 vs 集成测试

| 类型 | 测试范围 | 速度 | 适用场景 |
|------|---------|------|---------|
| 单元测试 | 单个函数/组件 | 快 | 业务逻辑、工具函数 |
| 集成测试 | 模块间交互 | 中 | API 端点、组件集成 |
| E2E 测试 | 完整流程 | 慢 | 关键用户流程 |

**策略**：大部分用单元测试，关键流程用 E2E 测试。

### 2. 测试命名规范

```python
# 清晰的测试名：test_<被测对象>_<场景>_<期望结果>
def test_user_service_decrement_quota_when_quota_is_positive_reduces_remaining():
    pass

# 前端：describe("组件名", () => { it("场景 期望结果", () => {}) })
describe("QuotaButton", () => {
  it("should disable button when quota is zero", () => {})
})
```

### 3. 测试覆盖的目标

- 核心业务逻辑：100%
- API 端点：>90%
- 工具函数：100%
- UI 组件：>80%

### 4. Mock 的使用原则

- 只 Mock 外部依赖（API 调用、数据库、LLM）
- 不要 Mock 被测试的类内部方法
- 集成测试中尽量少用 Mock

---

## 常见问题与解决方案

### Q: 如何测试异步代码？

```python
# 后端
@pytest.mark.asyncio
async def test_async_quota_operation():
    result = await quota_service.get_quota_async()
    assert result.remaining > 0
```

```typescript
// 前端
it('should handle async quota fetch', async () => {
  const { result } = renderHook(() => useQuota())
  await waitFor(() => {
    expect(result.current.remaining).toBe(3)
  })
})
```

### Q: 如何测试 LLM 集成？

```python
# 使用 Mock，不调用真实 LLM
from unittest.mock import AsyncMock

@pytest.fixture
def mock_llm_service():
    service = LLMService()
    service.validate_question = AsyncMock(
        return_value={"suitable": True, "reason": "Valid question"}
    )
    return service

async def test_question_validation_with_mock(mock_llm_service):
    result = await mock_llm_service.validate_question("我的未来如何？")
    assert result["suitable"] is True
```

### Q: 如何测试支付流程？

```python
# 使用 Stripe 测试模式 webhook
@pytest.fixture
def stripe_test_webhook():
    return {
        "event": "payment_intent.succeeded",
        "data": {
            "object": {"amount": 9900, "currency": "usd"}
        }
    }

async def test_payment_success_updates_subscription(stripe_test_webhook):
    response = await payment_service.handle_webhook(stripe_test_webhook)
    assert response.status == "success"
```

---

## 提交规范

每个提交应包含测试和生产代码：

```bash
# 典型的提交流程
git add tests/test_quota.py
git commit -m "test: add failing test for quota decrement [red]"

git add src/services/quota_service.py
git commit -m "feat: implement quota decrement [green]"

git add src/services/quota_service.py  # 重构后
git commit -m "refactor: extract quota management logic [refactor]"
```

---

## 检查清单

在完成功能开发前，确认：

- [ ] 所有新增代码都有对应的测试
- [ ] 所有测试通过（`pytest` 或 `npm test`）
- [ ] 测试覆盖率达标
- [ ] 没有硬编码的测试数据（使用 fixtures）
- [ ] Mock 使用合理（没有过度 Mock）
- [ ] 测试名称清晰，能反映测试意图
- [ ] 代码风格检查通过（ruff / eslint）
