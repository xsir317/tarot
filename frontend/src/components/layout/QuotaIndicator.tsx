'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { useUserStore } from '@/stores/useUserStore';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export function QuotaIndicator() {
  const { isAuthenticated, user } = useUserStore();
  const [quota, setQuota] = useState<{ remaining: number; total: number } | null>(null);

  useEffect(() => {
    // Fetch quota on mount
    const fetchQuota = async () => {
      try {
        const res = await apiClient.get('/quota');
        setQuota(res.data.data);
      } catch (err) {
        console.error('Failed to fetch quota', err);
      }
    };
    fetchQuota();
  }, [isAuthenticated]); // Refetch when auth state changes

  if (!quota) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex items-center gap-4 bg-slate-900/80 backdrop-blur-md p-2 rounded-full border border-slate-700 shadow-lg">
      <div className="px-3 flex flex-col items-end">
        <span className="text-xs text-slate-400 uppercase tracking-wider">Readings</span>
        <span className={`font-bold font-mono ${quota.remaining === 0 ? 'text-red-400' : 'text-emerald-400'}`}>
          {quota.remaining} / {quota.total}
        </span>
      </div>
      
      {quota.remaining === 0 && (
        <Button size="sm" variant="destructive" asChild>
          <Link href="/pricing">Get More</Link>
        </Button>
      )}

      {isAuthenticated ? (
         <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-xs font-bold">
            {user?.nickname?.charAt(0) || 'U'}
         </div>
      ) : (
        <Button size="sm" variant="secondary" asChild>
          <Link href="/auth/login">Login</Link>
        </Button>
      )}
    </div>
  );
}
