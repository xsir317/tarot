import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { TarotCard } from '@/components/tarot/TarotCard'
import type { Card } from '@/types/tarot'

const mockCard: Card = {
  id: '0',
  name: 'The Fool',
  nameEn: 'The Fool',
  suit: 'major',
  number: 0,
  meaning: {
    upright: 'New beginnings',
    reversed: 'Recklessness',
  },
}

// Mock framer-motion
vi.mock('framer-motion', () => ({
  motion: {
    button: ({ children, onClick, className, style }: any) => (
      <button className={className} onClick={onClick} style={style}>
        {children}
      </button>
    ),
  },
}))

describe('TarotCard', () => {
  it('should render card back when not flipped', () => {
    render(<TarotCard card={mockCard} isFlipped={false} />)
    const cardElement = document.querySelector('.tarot-card')
    expect(cardElement).toBeDefined()
    // Should not show card name when not flipped
    expect(screen.queryByText('The Fool')).not.toBeInTheDocument()
  })

  it('should render card front when flipped', () => {
    render(<TarotCard card={mockCard} isFlipped={true} />)
    expect(screen.getAllByText('The Fool')).toHaveLength(2)
  })

  it('should call onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<TarotCard card={mockCard} isFlipped={false} onClick={handleClick} />)
    const card = screen.getByRole('button')
    fireEvent.click(card)
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
