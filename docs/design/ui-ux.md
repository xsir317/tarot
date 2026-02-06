# UI/UX Design

## Design System
- **Colors**: Mystical & Calm
  - Primary: Deep Purple / Midnight Blue
  - Accent: Gold / Silver (for cards and highlights)
  - Background: Dark gradient
- **Typography**: Serif for headings (Elegant), Sans-serif for body (Readable).

## Core User Experience

### 1. Immersive Flow
The tarot reading is a ritual. Transitions should be smooth and deliberate, not instant.
- **Input**: Clean, focused.
- **Shuffling**: Visually satisfying, builds anticipation.
- **Drawing**: User feels control (e.g., "Stop" button or manual pick).
- **Revealing**: Click-to-flip, one by one.

### 2. Mobile First
- All animations must be optimized for touch.
- Cards must be legible on small screens.
- Touch targets >= 44px.

### 3. Feedback
- Loading states (skeleton screens or mystical spinners).
- Error toasts (gentle, not alarming).
- Success feedback (subtle glow or particle effects).

## Component Guidelines

### TarotCard
- **Props**: `cardId`, `position`, `isRevealed`, `onClick`
- **States**: FaceDown, FaceUp (Upright/Reversed)
- **Animation**: 3D Flip effect.

### ProgressBoard
- Visual indicator of current stage (Input -> Shuffle -> Result).
- Optional: "Step x of 3".

### QuotaIndicator
- Subtle display of remaining free readings.
- Turns red/alert when 0.
