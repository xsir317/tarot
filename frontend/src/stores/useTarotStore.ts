import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type TarotStage = 'input' | 'shuffling' | 'drawing' | 'revealing' | 'result';

export interface Card {
  id: string;
  name_key: string; // Updated to match backend
  position: 'upright' | 'reversed';
  image: string; // Updated to match backend
  isRevealed?: boolean;
}

export interface Interpretation {
  index: number;
  card_name: string;
  text: string;
}

interface TarotState {
  stage: TarotStage;
  question: string;
  cards: Card[];
  interpretations: Interpretation[];
  readingId: string | null;
  overallInterpretation: string | null;
  isInterpreting: boolean;
  
  setStage: (stage: TarotStage) => void;
  setQuestion: (q: string) => void;
  setCards: (cards: Card[]) => void;
  revealCard: (index: number) => void;
  setIsInterpreting: (loading: boolean) => void;
  setInterpretations: (interps: Interpretation[], id: string, overall: string) => void;
  reset: () => void;
}

export const useTarotStore = create<TarotState>()(
  persist(
    (set) => ({
      stage: 'input',
      question: '',
      cards: [],
      interpretations: [],
      readingId: null,
      overallInterpretation: null,
      isInterpreting: false,

      setStage: (stage) => set({ stage }),
      setQuestion: (question) => set({ question }),
      setCards: (cards) => set({ cards: cards.map(c => ({ ...c, isRevealed: false })) }),
      revealCard: (index) => set((state) => {
        const newCards = [...state.cards];
        if (newCards[index]) {
          newCards[index] = { ...newCards[index], isRevealed: true };
        }
        return { cards: newCards };
      }),
      setIsInterpreting: (isInterpreting) => set({ isInterpreting }),
      setInterpretations: (interpretations, readingId, overallInterpretation) => 
        set({ interpretations, readingId, overallInterpretation, isInterpreting: false }),
      reset: () => set({
        stage: 'input',
        question: '',
        cards: [],
        interpretations: [],
        readingId: null,
        overallInterpretation: null,
        isInterpreting: false
      }),
    }),
    {
      name: 'tarot-storage',
      partialize: (state) => ({ 
        stage: state.stage, 
        question: state.question, 
        cards: state.cards,
        interpretations: state.interpretations,
        readingId: state.readingId,
        overallInterpretation: state.overallInterpretation
      }),
    }
  )
);
