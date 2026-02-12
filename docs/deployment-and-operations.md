# 部署与运维指南

本文档详细说明了如何构建和运行 Tarot 项目的开发与生产环境。

## 1. 开发环境配置

### 1.1 Docker 环境 (后端与基础设施)

项目使用 Docker Compose 管理后端服务及数据库、缓存等基础设施。

#### 构建与重构镜像
如果你修改了后端代码或 `Dockerfile`，需要重新构建镜像：

> **注意**：为了在特定网络环境下加快构建速度，后端 `Dockerfile` 使用了自定义的 `backend/sources.list`（阿里云镜像源）。如果构建时遇到网络问题，请确保该文件内容正确。

```bash
# 构建镜像
docker-compose build

# 强制不使用缓存重新构建（适用于依赖更新或构建环境清理）
docker-compose build --no-cache
```

#### 运行环境
启动所有后端相关服务：

```bash
# 后台启动服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 停止环境
```bash
# 停止并移除容器
docker-compose down

# 停止并移除容器及数据卷（注意：这会删除数据库数据）
docker-compose down -v
```

### 1.2 客户端运行 (Frontend)

前端基于 Next.js 开发，通常在本地宿主机运行以便于开发调试。

#### 安装依赖
```bash
cd frontend
npm install
```

#### 运行开发服务器
```bash
npm run dev
```
访问地址：`http://localhost:3000`

### 1.3 调试指南

#### 后端调试
1. **容器内调试**：通过 `docker-compose logs -f backend` 查看实时日志。
2. **本地调试**：
   - 确保 Docker 中的 Postgres 和 Redis 已启动。
   - 在 `backend/` 目录下创建 `.env` 文件（参考 `.env.example`）。
   - 运行：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`。
   - 使用 VS Code 的 Python Debugger 附加到进程。

#### 前端调试
- **浏览器调试**：使用 Chrome DevTools 查看网络请求和 React 组件状态。
- **VS Code 调试**：配置 `launch.json` 使用 Debugger for Chrome/Edge 调试 Next.js。
- **日志输出**：查看终端运行 `npm run dev` 的控制台输出。

---

## 2. 生产环境构建与发布

### 2.1 后端构建与发布

生产环境建议使用 Docker 镜像进行部署。

#### 构建生产镜像
```bash
cd backend
docker build -t tarot-backend:latest .
```

#### 发布镜像
将镜像推送到你的镜像仓库（如 Docker Hub, AWS ECR, 阿里云镜像服务等）：
```bash
docker tag tarot-backend:latest your-registry.com/tarot-backend:v1.0.0
docker push your-registry.com/tarot-backend:v1.0.0
```

### 2.2 客户端构建与发布

前端需要进行静态编译或 SSR 构建。

#### 编译生产版本
```bash
cd frontend
npm run build
```

#### 发布生产版本
- **Vercel/Netlify**：直接连接 GitHub 仓库进行自动化部署（推荐）。
- **私有服务器**：
  - 构建后运行 `npm start`。
  - 或者使用 Docker 部署（需补充 Frontend Dockerfile）。
  - 或者导出静态站点（如果配置为 `output: 'export'`）。

### 2.3 更新与备份

#### 系统更新流程
1. **拉取最新代码**：`git pull origin main`
2. **后端更新**：
   ```bash
   docker-compose up -d --build backend
   # 运行数据库迁移
   docker-compose exec backend alembic upgrade head
   ```
3. **前端更新**：
   ```bash
   cd frontend
   npm install
   npm run build
   # 重启前端服务进程 (如使用 pm2)
   pm2 restart tarot-frontend
   ```

#### 数据备份
定期备份 PostgreSQL 数据库是非常重要的。

**手动备份**：
```bash
docker exec tarot-postgres pg_dump -U tarot_user tarot_db > backup_$(date +%Y%m%d).sql
```

**恢复数据**：
```bash
cat backup_xxx.sql | docker exec -i tarot-postgres psql -U tarot_user -d tarot_db
```

#### Redis 备份
Redis 数据通常作为缓存，但如果包含会话信息，可以通过备份 `dump.rdb` 文件进行：
```bash
docker cp tarot-redis:/data/dump.rdb ./redis_backup.rdb
```
