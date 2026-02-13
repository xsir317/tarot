import { useTranslations } from 'next-intl';
import Link from 'next/link';

export default function Home() {
  const t = useTranslations('Index');

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-slate-900 to-slate-950 text-white">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm lg:flex flex-col gap-8">
        <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
          {t('title')}
        </h1>
        <p className="text-xl text-slate-300">
          {t('subtitle')}
        </p>
        
        <div className="flex gap-4 mt-8">
          <Link 
            href="question" 
            className="px-8 py-4 bg-purple-600 hover:bg-purple-700 rounded-lg text-lg font-semibold transition-all shadow-lg hover:shadow-purple-500/20"
          >
            {t('start_button')}
          </Link>
          
          <Link 
            href="auth/login" 
            className="px-8 py-4 bg-slate-800 hover:bg-slate-700 rounded-lg text-lg font-semibold transition-all"
          >
            {t('login_button')}
          </Link>
        </div>
      </div>
    </main>
  );
}
