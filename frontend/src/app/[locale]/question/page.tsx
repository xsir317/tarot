'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { useLocale } from 'next-intl';
import { useTarotStore } from '@/stores/useTarotStore';
import { apiClient } from '@/lib/api-client';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

export default function QuestionPage() {
  const t = useTranslations('Tarot');
  const locale = useLocale();
  const router = useRouter();
  const { setQuestion, setStage, setCards, setIsInterpreting, setInterpretations } = useTarotStore();
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    try {
      // 1. Validate question
      const res = await apiClient.post('/tarot/validate', { 
        question: input,
        language: locale
      });
      
      if (res.data.data.suitable) {
        setQuestion(input);
        setStage('shuffling');
        
        // 2. Optimization: Draw cards and start interpretation immediately
        const drawRes = await apiClient.post('/tarot/draw');
        const drawnCards = drawRes.data.data.cards;
        setCards(drawnCards);
        
        setIsInterpreting(true);
        // Start interpretation in background, don't await it
        apiClient.post('/tarot/interpret', {
          question: input,
          cards: drawnCards.map((c: any) => ({ id: c.id, name: c.name_key, position: c.position })),
          language: locale
        }).then(interpRes => {
          const { interpretations, reading_id, overall_interpretation } = interpRes.data.data;
          setInterpretations(interpretations, reading_id, overall_interpretation);
        }).catch(err => {
          console.error("Background interpretation failed", err);
          setIsInterpreting(false);
        });

        router.push(`/${locale}/tarot/reading`);
      } else {
        alert(res.data.data.reason);
      }
    } catch (err: any) {
      console.error(err);
      const errorMsg = err.response?.data?.message || err.message || "Failed to validate question";
      alert(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 p-4 text-white">
      <div className="max-w-2xl w-full space-y-8">
        <h1 className="text-4xl font-serif text-center bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
          {t('question_title')}
        </h1>
        
        <div className="relative">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('input_placeholder')}
            className="w-full h-40 p-6 rounded-xl bg-slate-900/50 border border-slate-700 text-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
            maxLength={200}
          />
          <div className="absolute bottom-4 right-4 text-slate-500 text-sm">
            {input.length}/200
          </div>
        </div>

        <Button 
          onClick={handleSubmit}
          disabled={!input.trim() || loading}
          className="w-full py-6 text-xl bg-purple-600 hover:bg-purple-700 transition-all shadow-lg shadow-purple-900/20"
        >
          {loading ? t('consulting_spirits') : t('begin_reading')}
        </Button>
      </div>
    </div>
  );
}
