# Frontend Architecture

## Tech Stack
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod
- **I18n**: next-intl

## Directory Structure
```
frontend/
├── src/
│   ├── app/          # Pages & Layouts (App Router)
│   ├── components/   # React Components
│   │   ├── ui/       # Generic UI (shadcn)
│   │   └── tarot/    # Domain Components (Card, Deck)
│   ├── hooks/        # Custom Hooks
│   ├── lib/          # Utilities (API client, utils)
│   ├── stores/       # Zustand Stores
│   └── types/        # TS Interfaces
```

## State Management (Zustand)

### 1. UserStore
- `user`: User profile
- `token`: Access token
- `isAuthenticated`: bool
- `login(phone, code)`
- `logout()`

### 2. TarotStore
- `stage`: input -> shuffling -> drawing -> revealing -> result
- `question`: string
- `cards`: Array<Card>
- `interpretations`: Array<Interpretation>
- `reset()`

## Key Technical Decisions

### 1. API Client
- Centralized `fetch` wrapper with interceptors.
- Automatic token refresh on 401.

### 2. Animations
- **Shuffling**: Complex sequence using Framer Motion `AnimatePresence` and `layoutId`.
- **Card Flip**: CSS 3D transform or Framer Motion `rotateY`.

### 3. Internationalization
- Route-based i18n (`/en/...`, `/zh/...`) or Cookie-based.
- JSON translation files in `messages/`.
