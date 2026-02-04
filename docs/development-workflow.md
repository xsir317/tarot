# 开发工作流程

## 概述

本项目使用 Git Worktree 实现前后端并行开发。每个模块有独立的工作目录，可以同时修改代码，互不干扰。

---

## 项目结构

```
tarot/                    # 主仓库（main 分支 - 文档、配置）
├── docs/
├── CLAUDE.md
├── docker-compose.yml
└── ...

tarot-frontend/            # worktree - 前端开发（feature-frontend-* 分支）
└── frontend/
    ├── app/
    ├── components/
    └── ...

tarot-backend/             # worktree - 后端开发（feature-backend-* 分支）
└── backend
    ├── app/
    ├── tests/
    └── ...
```

---

## 初始化 Git Worktree

### 1. 创建分支

在主仓库（tarot/）中：

```bash
git checkout -b feature-frontend-init
git checkout -b feature-backend-init
git checkout main
```

### 2. 创建 Worktree

```bash
# 创建前端 worktree
git worktree add ../tarot-frontend feature-frontend-init

# 创建后端 worktree
git worktree add ../tarot-backend feature-backend-init
```

### 3. 验证

```bash
git worktree list
```

输出：
```
C:/Users/hujie/Documents/tarot           a259661 [main]
C:/Users/hujie/Documents/tarot-backend   a259661 [feature-backend-init]
C:/Users/hujie/Documents/tarot-frontend  a259661 [feature-frontend-init]
```

---

## 开发窗口设置

### 打开多个窗口并行开发

```
窗口 1: 主仓库 (tarot/)           - 负责文档、配置、合并代码
窗口 2: 前端 (tarot-frontend/)    - 负责前端开发
窗口 3: 后端 (tarot-backend/)     - 负责后端开发
窗口 4: Docker Compose           - 运行和联调
```

**推荐 IDE 配置:**
- 窗口 1: VS Code - 主仓库
- 窗口 2: VS Code - 前端
- 窗口 3: VS Code - 后端
- 窗口 4: 终端 - Docker Compose

---

## 完整开发流程

### 阶段 1：接口定义（主仓库）

在 `tarot/` 窗口中：

1. 编辑 API 设计文档
   ```bash
   docs/design/api-design.md
   ```

2. 提交到 main 分支
   ```bash
   git add docs/design/api-design.md
   git commit -m "docs: add /tarot/validate-question API design"
   git push origin main
   ```

3. 通知前后端开发者接口已更新

### 阶段 2：并行开发

#### 前端开发（tarot-frontend/ 窗口）

```bash
# 1. 同步最新的文档和 API 定义
git checkout feature-frontend-init
git pull origin main

# 2. 创建功能分支
git checkout -b feature-tarot-card-component

# 3. 按照 TDD 流程开发
#    - 编写测试（红）
#    - 实现功能（绿）
#    - 重构代码

# 4. 提交代码
git add .
git commit -m "feat: add TarotCard component with flip animation"
git push origin feature-tarot-card-component

# 5. 创建 Pull Request
#    - 请求合并到 feature-frontend-init
```

#### 后端开发（tarot-backend/ 窗口）

```bash
# 1. 同步最新的文档和 API 定义
git checkout feature-backend-init
git pull origin main

# 2. 创建功能分支
git checkout -b feature-validate-question-api

# 3. 按照 TDD 流程开发
#    - 编写测试（红）
#    - 实现功能（绿）
#    - 重构代码

# 4. 提交代码
git add .
git commit -m "feat: add /r/validate-question endpoint with LLM integration"
git push origin feature-validate-question-api

# 5. 创建 Pull Request
#    - 请求合并到 feature-backend-init
```

### 阶段 3：联调测试

在 Docker Compose 窗口中：

```bash
# 1. 启动所有服务
cd tarot/
docker-compose up -d

# 2. 查看日志
docker-compose logs -f

# 3. 运行 E2E 测试
docker-compose exec frontend npm run test:e2e
```

### 阶段 4：合并代码

在主仓库（tarot/）窗口中：

```bash
# 1. 合并前端代码
git checkout main
git pull origin main
git merge feature-frontend-init
git push origin main

# 2. 合并后端代码
git checkout main
git pull origin main
git merge feature-backend-init
git push origin main
```

---

## 文档同步策略

### 文档位置

所有文档在主仓库的 `docs/` 目录下，三个 worktree 自动同步。

### 推荐做法

1. **在主仓库修改文档**
   ```bash
   # 在 tarot/ 窗口中
   vim docs/design/api-design.md
   git add docs/
   git commit -m "docs: update API design"
   git push origin main
   ```

2. **前后端获取更新**
   ```bash
   # 在 tarot-frontend/ 和 tarot-backend/ 窗口中
   git pull origin main
   ```

3. **不在 worktree 中修改文档**
   - 如果必须修改，先提交到功能分支
   - 再合并到 main

---

## Worktree 常用命令

### 查看所有 Worktree

```bash
git worktree list
```

### 创建新 Worktree

```bash
# 创建新的功能 worktree
git worktree add ../tarot-feature feature-new-feature
```

### 删除 Worktree

```bash
# 删除 worktree（完成开发后）
git worktree remove ../tarot-frontend
git worktree remove ../tarot-backend
```

### 清理已删除的分支

```bash
# 清理已合并或删除的分支对应的 worktree
git worktree prune
```

### 移动 Worktree

```bash
# 移动 worktree 到新位置
git worktree move ../[old-location] ../[new-location]
```

---

## 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|---------|---------|------|
| 前端初始化 | `feature-frontend-init` | - |
| 后端初始化 | `feature-backend-init` | - |
| 前端功能 | `feature-frontend-*` | `feature-frontend-tarot-card` |
| 后端功能 | `feature-backend-*` | `feature-backend-validate-api` |
| 修复 | `fix-*` | `fix-quota-bug` |
| 文档 | `docs-*` | `docs-api-update` |

---

## 提交消息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
[type] subject

body

footer

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `test` | 添加测试 |
| `chore` | 构建/工具 |

---

## 冲突解决

### Worktree 之间的冲突

当多个 worktree 修改同一文件时：

```bash
# 在主仓库中合并
git checkout main
git merge feature-frontend-init

# 如果有冲突，解决后
git add .
git commit -m "resolve: merge conflicts from feature-frontend-init"
```

### 解决冲突后同步到 Worktree

```bash
# 在其他 worktree 中
git checkout main
git pull origin main
```

---

## TDD 工作流程

每个工作区都遵循 TDD 红绿重构循环：

详细规范请参考：**`docs/tdd-workflow.md`**

```
1. 红 - 编写失败的测试
2. 绿 - 编写最简代码通过测试
3. 重构 - 优化代码结构
```

---

## 示例：实现"问题验证"功能

### 1. 在主仓库定义接口

```bash
# tarot/ 窗口
vim docs/design/api-design.md
# 添加 POST /tarot/validate-question API 定义

git add docs/
git commit -m "docs: add validate-question API design"
git push origin main
```

### 2. 后端实现 API

```bash
# tarot-backend/ 窗口
git checkout feature-backend-init
git pull origin main
git checkout -b feature-validate-question

# 按照 TDD 流程开发
#    1. 编写测试（tests/test_tarot.py）
#    2. 实现功能（app/api/tarot.py）
#    3. 重构代码

git add .
git commit -m "feat: add /tarot/validate-question endpoint"
git push origin feature-validate-question
```

### 3. 前端调用 API

```bash
# tarot-frontend/ 窗口
git checkout feature-frontend-init
git pull origin main
git checkout -b feature-validate-question-ui

# 按照 TDD 流程开发
#    1. 编写测试
#    2. 实现调用 API
#    3. 重构代码

git add .
git commit -m "feat: add question validation UI"
git push origin feature-validate-question-ui
```

### 4. 联调测试

```bash
# Docker Compose 窗口
cd tarot/
docker-compose up -d
docker-compose exec frontend npm run test:e2e
```

### 5. 合并代码

```bash
# tarot/ 窗口
git checkout main
git pull origin main

# 合并前端
git merge feature-frontend-init
git push origin main

# 合并后端
git merge feature-backend-init
git push origin main
```

---

## 清理 Worktree

项目完成后，清理 worktree：

```bash
# 1. 删除 worktree
git worktree remove ../tarot-frontend
git worktree remove ../tarot-backend

# 2. 删除分支
git branch -D feature-frontend-init
git branch -D feature-backend-init

# 3. 清理
git worktree prune
```

---

## 注意事项

1. **不要在多个 worktree 中同时修改同一文件**
   - 会导致冲突，难以解决
   - 特别是 `docs/` 和配置文件

2. **定期同步主仓库**
   - 前后端定期 `git pull origin main`
   - 获取最新的文档和 API 定义

3. **保持分支简洁**
   - 功能完成后及时合并
   - 不要在功能分支上堆积太多提交

4. **使用 Git Hooks**
   - 配置 pre-commit hooks 自动格式化
   - 配置 commit-msg hooks 验证提交消息格式
