'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTarotStore } from '@/stores/useTarotStore';
import { apiClient } from '@/lib/api-client';
import { TarotCard } from '@/components/tarot/TarotCard';
import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';

export default function ReadingPage() {
  const t = useTranslations('Tarot');
  const { 
    stage, 
    setStage, 
    cards, 
    setCards, 
    revealCard, 
    question,
    setInterpretations,
    overallInterpretation,
    interpretations
  } = useTarotStore();
  
  const [loading, setLoading] = useState(false);

  // Auto-start shuffling when entering page
  useEffect(() => {
    if (stage === 'shuffling') {
      const timer = setTimeout(() => {
        setStage('drawing');
      }, 3000); // Shuffle for 3s
      return () => clearTimeout(timer);
    }
  }, [stage, setStage]);

  const handleDraw = async () => {
    setLoading(true);
    try {
      const res = await apiClient.post('/tarot/draw');
      setCards(res.data.data.cards);
      setStage('revealing');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReveal = async (index: number) => {
    if (cards[index].isRevealed) return;
    
    revealCard(index);
    
    // Check if all cards revealed
    const allRevealed = cards.every((c, i) => i === index || c.isRevealed);
    if (allRevealed) {
      // Fetch interpretation
      try {
        const res = await apiClient.post('/tarot/interpret', {
          question,
          cards: cards.map(c => ({ id: c.id, name: c.name, position: c.position })),
          language: 'zh'
        });
        const { interpretations, reading_id, overall_interpretation } = res.data.data;
        setInterpretations(interpretations, reading_id, overall_interpretation);
        setStage('result');
      } catch (err) {
        console.error("Failed to interpret", err);
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center py-8 overflow-hidden">
      {/* Header */}
      <div className="text-center mb-8 px-4 z-10">
        <h2 className="text-xl text-purple-300 font-serif mb-2">Question</h2>
        <p className="text-white text-lg italic opacity-80 max-w-xl mx-auto">"{question}"</p>
      </div>

      {/* Main Stage Area */}
      <div className="flex-1 w-full max-w-4xl flex items-center justify-center relative min-h-[500px]">
        <AnimatePresence mode='wait'>
          
          {/* Shuffling Stage */}
          {stage === 'shuffling' && (
            <motion.div 
              key="shuffling"
              className="relative"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {[0, 1, 2, 3, 4].map((i) => (
                <motion.div
                  key={i}
                  className="absolute top-0 left-0"
                  animate={{ 
                    x: [0, Math.random() * 20 - 10, 0],
                    y: [0, Math.random() * 20 - 10, 0],
                    rotate: [0, Math.random() * 10 - 5, 0]
                  }}
                  transition={{ repeat: Infinity, duration: 0.5, delay: i * 0.1 }}
                >
                  <TarotCard width={120} height={200} />
                </motion.div>
              ))}
              <div className="mt-64 text-purple-300 animate-pulse">Shuffling the deck...</div>
            </motion.div>
          )}

          {/* Drawing Stage */}
          {stage === 'drawing' && (
            <motion.div 
              key="drawing"
              className="flex flex-col items-center gap-8"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <div className="flex gap-[-50px]">
                {/* Deck Stack Visual */}
                <div className="relative">
                  <TarotCard width={140} height={240} className="shadow-2xl" />
                  <div className="absolute top-1 left-1 -z-10 w-full h-full bg-slate-800 rounded-xl border border-slate-700" />
                  <div className="absolute top-2 left-2 -z-20 w-full h-full bg-slate-800 rounded-xl border border-slate-700" />
                </div>
              </div>
              
              <Button 
                size="lg"
                onClick={handleDraw} 
                disabled={loading}
                className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-serif px-12 py-6 text-xl rounded-full shadow-[0_0_20px_rgba(245,158,11,0.3)]"
              >
                {loading ? 'Drawing...' : t('draw_button')}
              </Button>
            </motion.div>
          )}

          {/* Revealing & Result Stage */}
          {(stage === 'revealing' || stage === 'result') && (
            <motion.div 
              key="revealing"
              className="w-full flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8 px-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {cards.map((card, index) => (
                <motion.div
                  key={card.id}
                  initial={{ y: 50, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: index * 0.2 }}
                >
                  <TarotCard 
                    card={card}
                    isRevealed={card.isRevealed}
                    onClick={() => handleReveal(index)}
                    width={180}
                    height={300}
                    className="hover:scale-105 transition-transform"
                  />
                  {card.isRevealed && (
                    <motion.div 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="mt-4 text-center"
                    >
                      <p className="font-serif text-amber-300">{card.name}</p>
                      <p className="text-xs text-slate-400 uppercase tracking-widest">{card.position}</p>
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Result Interpretation (Only visible in result stage) */}
      {stage === 'result' && (
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-4xl px-6 pb-20 mt-12"
        >
          <div className="bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-2xl p-8 shadow-2xl">
            <h3 className="text-3xl font-serif text-center mb-8 text-purple-200">The Oracle Speaks</h3>
            
            <div className="space-y-6 text-slate-200 leading-relaxed">
               {/* This would be populated from interpretations store */}
               <div className="p-4 bg-slate-800/50 rounded-lg border border-slate-700/50">
                 {overallInterpretation || "Consulting the stars..."}
               </div>
            </div>

            <div className="mt-8 flex justify-center gap-4">
               <Button variant="outline" onClick={() => window.location.href = '/'}>Home</Button>
               <Button className="bg-purple-600">Save Reading</Button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}
