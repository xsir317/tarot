# 组件设计

## 可复用组件清单

### 基础组件

- Button
- Input
- Textarea
- Select
- Card
- Modal
- Toast

### 业务组件

- TarotCard (塔罗牌)
- GenderSelector (性别选择器)
- QuotaIndicator (额度指示器)
- SubscriptionCard (订阅卡片)
- HistoryItem (历史记录项)

---

## TarotCard 组件

```typescript
interface TarotCardProps {
  card: Card
  isFlipped: boolean
  onClick?: () => void
}

export function TarotCard({ card, isFlipped, onClick }: TarotCardProps) {
  return (
    <motion.div
      className="tarot-card"
      onClick={onClick}
      animate={{ rotateY: isFlipped ? 180 : 0 }}
      transition={{ duration: 0.6 }}
    >
      {isFlipped ? <CardFront card={card} /> : <CardBack />}
    </motion.div>
  )
}
```

---

## QuotaIndicator 组件

```typescript
export function QuotaIndicator({ remaining, total }: QuotaIndicatorProps) {
  const percentage = (remaining / total) * 100

  return (
    <div className="quota-indicator">
      <span>免费次数: {remaining}/{total}</span>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  )
}
```

---

## 国际化支持

```typescript
import { useTranslations } from 'next-intl'

function MyComponent() {
  const t = useTranslations()
  return <h1>{t('home.title')}</h1>
}
```
