import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import QuestionPage from '@/app/question/page'

// Mock next/link
vi.mock('next/link', () => ({
  default: ({ children, href }: any) => <a href={href}>{children}</a>,
}))

describe('Question page', () => {
  it('should render question textarea', () => {
    render(<QuestionPage />)
    expect(screen.getByPlaceholderText(/请输入你的问题/i)).toBeInTheDocument()
  })

  it('should render start drawing button', () => {
    render(<QuestionPage />)
    expect(screen.getByText('开始抽牌')).toBeInTheDocument()
  })

  it('should render character count', () => {
    render(<QuestionPage />)
    expect(screen.getByText('0/200')).toBeInTheDocument()
  })
})
