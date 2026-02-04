'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function QuestionPage() {
  const [question, setQuestion] = useState('')
  const maxLength = 200

  const handleSubmit = () => {
    // TODO: validate question with API
    if (question.trim()) {
      window.location.href = '/shuffling'
    }
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-indigo-50 to-purple-100 p-24 dark:from-gray-900 dark:to-indigo-900">
      <div className="w-full max-w-md space-y-6">
        <h1 className="text-3xl font-bold text-center text-purple-900 dark:text-purple-100">
          请输入你的问题
        </h1>
        <p className="text-center text-purple-600 dark:text-purple-300">
          塔罗牌将为你揭示答案
        </p>
        <div className="space-y-3">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="请输入你的问题..."
            maxLength={maxLength}
            className="w-full h-40 p-4 border-2 border-purple-300 rounded-lg focus:border-purple-500 focus:outline-none resize-none bg-white dark:bg-gray-800 dark:border-purple-600 dark:text-white"
          />
          <div className="flex justify-between items-center">
            <span className="text-sm text-purple-600 dark:text-purple-300">
              {question.length}/{maxLength}
            </span>
          </div>
        </div>
        <button
          onClick={handleSubmit}
          disabled={!question.trim()}
          className="w-full py-3 text-lg bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:bg-purple-400 disabled:cursor-not-allowed shadow-lg"
        >
          开始抽牌
        </button>
        <div className="text-center">
          <Link href="/" className="text-sm text-purple-600 hover:text-purple-700 dark:text-purple-300">
            返回首页
          </Link>
        </div>
      </div>
    </main>
  )
}
