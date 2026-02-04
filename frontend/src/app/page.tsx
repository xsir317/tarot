import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-purple-50 to-indigo-100 p-24 dark:from-gray-900 dark:to-purple-900">
      <div className="text-center space-y-8">
        <h1 className="text-4xl md:text-5xl font-bold text-purple-900 dark:text-purple-100">
          开启你的心灵指引之旅
        </h1>
        <Link href="/question">
          <button className="mt-4 px-8 py-3 text-lg bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors shadow-lg hover:shadow-xl">
            开始占卜
          </button>
        </Link>
      </div>
    </main>
  )
}
