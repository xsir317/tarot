import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { QuotaIndicator } from '@/components/layout/QuotaIndicator';
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Mystic Tarot",
  description: "AI-powered Tarot Reading",
}

export default async function RootLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body className={`${inter.className} bg-slate-950 text-slate-100 min-h-screen`}>
        <NextIntlClientProvider messages={messages}>
          <QuotaIndicator />
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
