# 页面跳转逻辑

## 页面列表

1. 首页 (/)
2. 问题输入页 (/question)
3. 洗牌动画页 (/shuffling)
4. 翻牌互动页 (/reading)
5. 解读结果页 (/result/:readingId)
6. 注册页 (/register)
7. 付费页面 (/payment)
8. 用户中心 (/account)

---

## 页面跳转流程

```
首页
  ↓ [开始占卜]
问题输入页
  ↓ [开始抽牌]
  ├─→ [问题不适合] → 弹窗提示 → 返回
  └─→ [问题适合]
       → 洗牌动画页
       → 翻牌互动页
       ↓ [翻完3张]
       ├─→ [有额度] → 解读结果页
       └─→ [无额度]
            ├─→ [已登录] → 付费页面 → 解读结果页
            └─→ [未登录] → 注册弹窗
```

---

## Next.js 路由示例

```typescript
// app/page.tsx - 首页
export default function HomePage() {
  return (
    <>
      <h1>开启你的心灵指引之旅</h1>
      <Link href="/question">开始占卜</Link>
    </>
  )
}

// app/reading/page.tsx - 翻牌互动页
export default function ReadingPage() {
  const [flippedCards, setFlippedCards] = useState<number[]>([])

  const handleCardClick = (index: number) => {
    const newFlipped = [...flippedCards, index]
    setFlippedCards(newFlipped)

    if (newFlipped.length === 3) {
      router.push(`/result/${readingId}`)
    }
  }

  return (
    <div>
      {cards.map((card, index) => (
        <TarotCard
          key={index}
          isFlipped={flippedCards.includes(index)}
          onClick={() => handleCardClick(index)}
        />
      ))}
    </div>
  )
}
```
