## 现象与结论
- 你点“开始占卜”后进入的 `/question` 并不是“问题输入页”，而是被根路由动态段 `[locale]` 吞掉后渲染了首页，所以你看不到输入框。
- 真正的问题输入页在 `/:locale/question`，例如 `/zh/question` 或 `/en/question`，页面里已经有 `<textarea>` 输入框。

## 根因（对应你提到的两个问题）
- **主流程阻塞**：首页使用了绝对路径 `href="/question"`，导致访问 `/question` 时 Next.js 解释为 `/{locale}`（`locale="question"`），从而命中首页路由 `src/app/[locale]/page.tsx`。
- **语言不稳定**：当 `locale` 不是 `en|zh` 时，`src/i18n/request.ts` 会把 locale 回退成 `en`，所以“看起来像从中文跳到了英文”。
- **中间件未兜底**：`src/middleware.ts` 的 matcher 只匹配 `/` 和 `/(zh|en)/...`，不会处理 `/question` 这种“无 locale 前缀的非根路径”，所以不会把它纠正到 `/{locale}/question`。

## 修复方案（按优先级）
1. **让无前缀路径统一被 next-intl 中间件接管**
   - 扩大 `frontend/src/middleware.ts` 的 `config.matcher` 覆盖范围，让 `/question`、`/auth/login` 这类无前缀路径都能被重定向到 `/{locale}/...`（根据浏览器语言/默认语言）。
2. **在 `[locale]` 入口做强校验，避免“吞路径 + 默认英文”这种静默错误**
   - 在 `frontend/src/app/[locale]/layout.tsx` 中校验 `params.locale`，不是 `en|zh` 就直接 `notFound()`（或等价处理），防止把任意单段路径当成 locale。
3. **修正站内跳转为 locale 安全的写法，打通主流程**
   - `src/app/[locale]/page.tsx`：把 `href="/question"`、`href="/auth/login"` 改成带 locale 的写法（推荐用相对路径 `"question"` / `"auth/login"`，避免手写 locale）。
   - `src/components/layout/QuotaIndicator.tsx` 等：同样修正到相对路径或基于当前 locale 生成路径。
   - `src/app/[locale]/question/page.tsx`：把 `router.push('/tarot/reading')` 改成带 locale 的跳转（例如基于当前 locale 组装路径），否则会继续触发路由错误。
4. **补齐 i18n，消除页面内硬编码英文**
   - `question/page.tsx`、`tarot/reading/page.tsx`、`auth/login/page.tsx` 中把硬编码英文文案替换为 `useTranslations()` 的 key。
   - 在 `frontend/messages/zh.json` 与 `frontend/messages/en.json` 增加缺失的文案 key（例如标题、按钮 loading 文案、结果页标题等）。
   - 同时把接口参数里的 `language: 'zh'` 改为根据当前 locale 传递，保证解读语言和 UI 一致。

## 验证方式
- 手工验证：
  - 从 `/` 进入后点击“开始占卜”，应落到 `/{locale}/question` 且能看到输入框。
  - 直接访问 `/question` 也应自动变成 `/{locale}/question`（或至少不再渲染首页）。
  - 在 question → reading → home 全流程中语言保持一致。
- 自动化验证：
  - 补一个前端单测，断言首页“开始占卜”链接不会是 `"/question"` 这种无前缀绝对路径。
  - 跑 `frontend` 的 vitest 测试套件，确保不引入回归。

## 你现在的临时绕过方式（不改代码也能继续体验）
- 直接打开 `/zh/question`（或 `/en/question`）即可看到问题输入框并继续流程。