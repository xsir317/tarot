import { motion } from 'framer-motion'
import type { Card } from '@/types/tarot'

interface TarotCardProps {
  card: Card
  isFlipped: boolean
  onClick?: () => void
}

export function TarotCard({ card, isFlipped, onClick }: TarotCardProps) {
  return (
    <motion.button
      className="tarot-card relative w-32 h-48 cursor-pointer"
      onClick={onClick}
      animate={{ rotateY: isFlipped ? 180 : 0 }}
      transition={{ duration: 0.6, type: 'spring', stiffness: 100 }}
      style={{ perspective: 1000 }}
    >
      {isFlipped ? (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-white rounded-lg shadow-lg border-2 border-purple-300">
          <span className="text-lg font-semibold text-purple-900">{card.nameEn}</span>
          <span className="text-sm text-purple-600 mt-1">{card.name}</span>
        </div>
      ) : (
        <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-purple-800 to-indigo-900 rounded-lg shadow-lg">
          <div className="w-20 h-32 border-2 border-purple-300 rounded opacity-30" />
        </div>
      )}
    </motion.button>
  )
}
