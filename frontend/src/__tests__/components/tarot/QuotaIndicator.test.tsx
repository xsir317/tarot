import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { QuotaIndicator } from '@/components/tarot/QuotaIndicator'

describe('QuotaIndicator', () => {
  it('should render remaining quota count', () => {
    render(<QuotaIndicator remaining={3} total={3} />)
    expect(screen.getByText(/免费次数: 3\/3/)).toBeInTheDocument()
  })

  it('should render progress bar', () => {
    render(<QuotaIndicator remaining={2} total={3} />)
    const progressBar = document.querySelector('.progress-fill')
    expect(progressBar).toBeDefined()
  })

  it('should show full progress bar when quota is full', () => {
    const { container } = render(<QuotaIndicator remaining={3} total={3} />)
    const progressBar = container.querySelector('.progress-fill') as HTMLElement
    expect(progressBar?.style.width).toBe('100%')
  })

  it('should show partial progress bar', () => {
    const { container } = render(<QuotaIndicator remaining={1} total={3} />)
    const progressBar = container.querySelector('.progress-fill') as HTMLElement
    expect(progressBar?.style.width).toBe('33.33%')
  })
})
