'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { useLocale } from 'next-intl';
import { useUserStore } from '@/stores/useUserStore';
import { apiClient } from '@/lib/api-client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';

export default function LoginPage() {
  const t = useTranslations('Auth');
  const locale = useLocale();
  const router = useRouter();
  const login = useUserStore((state) => state.login);

  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [codeSent, setCodeSent] = useState(false);
  const [error, setError] = useState('');

  const handleSendCode = async () => {
    if (!phone) return;
    setLoading(true);
    setError('');
    try {
      const res = await apiClient.post('/auth/send-code', { phone });
      // In MVP, code is returned in response for testing
      const testCode = res.data?.data?.code;
      if (testCode) {
        // For developer convenience, auto-fill or log
        console.log('Test Code:', testCode);
        alert(`Test Code: ${testCode}`);
      }
      setCodeSent(true);
    } catch (err) {
      setError(t('send_code_failed'));
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    if (!phone || !code) return;
    setLoading(true);
    setError('');
    try {
      const res = await apiClient.post('/auth/login/code', { phone, code });
      const { access_token, refresh_token, user } = res.data.data;
      
      login(user, access_token, refresh_token);
      router.push(`/${locale}`);
    } catch (err) {
      setError(t('login_failed'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 p-4">
      <Card className="w-full max-w-md bg-slate-900 border-slate-800 text-slate-100">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            {t('login_title')}
          </CardTitle>
          <CardDescription className="text-center text-slate-400">
            {t('login_description')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="phone">{t('phone_label')}</Label>
            <div className="flex gap-2">
              <Input
                id="phone"
                placeholder="+1234567890"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="bg-slate-950 border-slate-800 focus:ring-purple-500"
              />
              <Button 
                variant="secondary" 
                onClick={handleSendCode}
                disabled={loading || !phone || codeSent}
              >
                {codeSent ? t('code_sent') : t('send_code')}
              </Button>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="code">{t('code_label')}</Label>
            <Input
              id="code"
              placeholder="123456"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="bg-slate-950 border-slate-800 focus:ring-purple-500"
            />
          </div>

          {error && <p className="text-red-500 text-sm">{error}</p>}
        </CardContent>
        <CardFooter>
          <Button 
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            onClick={handleLogin}
            disabled={loading || !code}
          >
            {loading ? t('loading') : t('login_button')}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
