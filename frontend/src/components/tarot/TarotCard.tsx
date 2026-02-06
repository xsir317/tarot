'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Card } from '@/stores/useTarotStore';

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
          <div className="absolute inset-2 border border-slate-800 rounded-lg opacity-50" />
          <div className="w-16 h-16 rounded-full border-2 border-purple-500/30 flex items-center justify-center">
            <div className="w-12 h-12 rounded-full border border-purple-500/50" />
          </div>
          {/* Pattern overlay */}
          <div className="absolute inset-0 bg-[url('/pattern.svg')] opacity-10 bg-repeat" />
        </div>

        {/* Card Front */}
        <div 
          className="absolute inset-0 backface-hidden rounded-xl bg-slate-100 text-slate-900 overflow-hidden shadow-xl"
          style={{ transform: 'rotateY(180deg)', backfaceVisibility: 'hidden' }}
        >
          {card ? (
            <div className={cn(
              "w-full h-full flex flex-col items-center justify-between p-4",
              card.position === 'reversed' && "rotate-180"
            )}>
              <div className="text-sm font-serif font-bold uppercase tracking-wider">{card.name_en}</div>
              <div className="flex-1 w-full flex items-center justify-center my-2 bg-slate-200 rounded-lg">
                {/* Image Placeholder */}
                <span className="text-4xl">🔮</span>
              </div>
              <div className="text-lg font-serif font-bold">{card.name}</div>
            </div>
          ) : null}
        </div>
      </motion.div>
    </div>
  );
}
