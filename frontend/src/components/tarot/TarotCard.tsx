'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Card } from '@/stores/useTarotStore';
import { useTranslations } from 'next-intl';

interface TarotCardProps {
  card?: Card;
  isRevealed?: boolean;
  onClick?: () => void;
  className?: string;
  width?: number;
  height?: number;
}

export function TarotCard({ 
  card, 
  isRevealed = false, 
  onClick, 
  className,
  width = 200,
  height = 340
}: TarotCardProps) {
  const t = useTranslations('Cards');

  return (
    <div 
      className={cn("relative perspective-1000 cursor-pointer", className)}
      style={{ width, height }}
      onClick={onClick}
    >
      <motion.div
        className="w-full h-full relative preserve-3d transition-all duration-500"
        initial={false}
        animate={{ rotateY: isRevealed ? 180 : 0 }}
        transition={{ duration: 0.6, type: "spring", stiffness: 260, damping: 20 }}
      >
        {/* Card Back */}
        <div 
          className="absolute inset-0 backface-hidden rounded-xl border-2 border-slate-700 bg-slate-900 flex items-center justify-center overflow-hidden shadow-xl"
          style={{ backfaceVisibility: 'hidden' }}
        >
          {/* Real Card Back Image */}
          <img 
            src="/cards/card_back.webp" 
            alt="Card Back" 
            className="w-full h-full object-cover"
          />
        </div>

        {/* Card Front */}
        <div 
          className="absolute inset-0 backface-hidden rounded-xl bg-slate-100 text-slate-900 overflow-hidden shadow-xl"
          style={{ transform: 'rotateY(180deg)', backfaceVisibility: 'hidden' }}
        >
          {card ? (
            <div className={cn(
              "w-full h-full flex flex-col items-center justify-between",
              card.position === 'reversed' && "rotate-180"
            )}>
              {/* Real Card Front Image */}
              <img 
                src={card.image || `/cards/${card.id}.webp`} 
                alt={t(card.name_key)} 
                className="w-full h-full object-cover"
              />
            </div>
          ) : null}
        </div>
      </motion.div>
    </div>
  );
}
