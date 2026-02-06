# 项目规则

## 目录结构

### 前端 (Frontend)
位于 `frontend/` 目录，基于 Next.js 14+ (App Router)。
- `src/app`: 页面路由和布局
- `src/components`: UI 组件
- `src/types`: TypeScript 类型定义

### 后端 (Backend)
位于 `backend/` 目录，基于 FastAPI (Python 3.11+)。
- `app/api`: API 路由定义
- `app/models`: SQLAlchemy 数据模型
- `app/schemas`: Pydantic 数据验证模式
- `app/services`: 业务逻辑服务
- `tests/`: 测试套件

## TDD 工作流

本项目严格遵循测试驱动开发 (TDD) 流程：
1. **红 (Red)**: 编写一个失败的测试用例。
2. **绿 (Green)**: 编写最少量的代码让测试通过。
3. **重构 (Refactor)**: 优化代码结构，确保测试依然通过。

详细规范请参考 `docs/tdd-workflow.md`。
