# 认证策略

## 概述

本项目采用 JWT（JSON Web Token）+ HTTP-only Cookies 的认证方案。

## Token 设计

### Access Token
- **有效期**: 15 分钟
- **用途**: 访问需要认证的 API
- **存储方式**: HTTP-only Cookie

### Refresh Token
- **有效期**: 7 天
- **用途**: 刷新 Access Token
- **存储方式**: 数据库（tokens 表）

## 认证流程

### 注册流程
```
输入邮箱/手机号 → 发送验证码 → 验证码验证 → 设置密码 → 注册成功
```

### 登录流程
```
输入邮箱/手机号 + 密码 → 验证 → 生成 Token → 登录成功
```

### 登出流程
```
检查 Token → 删除数据库中的 Refresh Token → 清除 Cookie → 登出成功
```

## 匿名用户识别

### 设备指纹策略
- FingerprintJS 生成浏览器指纹
- IP 地址
- localStorage 存储设备 ID

### 匿名用户额度
- **免费额度**: 3 次
- **有效期**: 7 天
- **存储**: Redis

## 安全措施

### 密码安全
- bcrypt 加密（12 rounds）

### Cookie 安全
- HTTP-only: 防止 XSS
- Secure: 仅 HTTPS
- SameSite: lax

### 速率限制
- /auth/send-code: 3 次/小时
- /auth/login: 10 次/小时
