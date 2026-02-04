# 动画设计规范

## 概述

使用 Framer Motion 实现流畅的动画效果。

---

## 动画类型

### 1. 洗牌动画

- 多张牌快速移动、交换位置
- 持续时间: 2-3 秒

```typescript
<motion.div
  animate={{
    x: (index - 2) * 80,
    y: Math.sin(index * 0.5) * 20
  }}
  transition={{ duration: 0.5, repeat: 3, repeatType: 'reverse' }}
>
  <CardBack />
</motion.div>
```

### 2. 翻牌动画

- 3D 翻转显示牌面
- 持续时间: 0.6 秒

```typescript
<motion.div
  animate={{ rotateY: isFlipped ? 180 : 0 }}
  transition={{ duration: 0.6, type: 'spring', stiffness: 100 }}
>
  {isFlipped ? <CardFront /> : <CardBack />}
</motion.div>
```

### 3. 解读淡入动画

```typescript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.8 }}
>
  {text}
</motion.div>
```

---

## 性能优化

```css
.animated-element {
  will-change: transform, opacity;
}
```

---

## 无障碍支持

```typescript
import { useReducedMotion } from 'framer-motion'

const shouldReduceMotion = useReducedMotion()
```
