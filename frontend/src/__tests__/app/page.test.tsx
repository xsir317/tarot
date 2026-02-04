import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

describe('Home page', () => {
  it('should render the main heading', () => {
    render(<Home />)
    expect(screen.getByText('开启你的心灵指引之旅')).toBeInTheDocument()
  })

  it('should render a start reading button', () => {
    render(<Home />)
    expect(screen.getByText('开始占卜')).toBeInTheDocument()
  })
})
