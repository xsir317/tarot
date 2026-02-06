import { describe, it, expect, beforeEach } from 'vitest';
import { useTarotStore } from '../../stores/useTarotStore';

describe('useTarotStore', () => {
  beforeEach(() => {
    useTarotStore.getState().reset();
  });

  it('should initialize with default state', () => {
    const state = useTarotStore.getState();
    expect(state.stage).toBe('input');
    expect(state.question).toBe('');
    expect(state.cards).toEqual([]);
    expect(state.interpretations).toEqual([]);
    expect(state.readingId).toBeNull();
  });

  it('should set question and advance stage', () => {
    useTarotStore.getState().setQuestion('Test question');
    expect(useTarotStore.getState().question).toBe('Test question');
    
    useTarotStore.getState().setStage('shuffling');
    expect(useTarotStore.getState().stage).toBe('shuffling');
  });

  it('should set cards', () => {
    const mockCards = [
      { id: 'fool', name: 'The Fool', position: 'upright' },
      { id: 'magician', name: 'The Magician', position: 'reversed' }
    ];
    useTarotStore.getState().setCards(mockCards as any);
    
    const expectedCards = mockCards.map(c => ({ ...c, isRevealed: false }));
    expect(useTarotStore.getState().cards).toEqual(expectedCards);
  });

  it('should update specific card revealed status', () => {
    const mockCards = [
      { id: 'fool', name: 'The Fool', position: 'upright', isRevealed: false },
    ];
    useTarotStore.getState().setCards(mockCards as any);
    
    useTarotStore.getState().revealCard(0);
    expect(useTarotStore.getState().cards[0].isRevealed).toBe(true);
  });
  
  it('should set interpretations', () => {
    const mockInterps = [{ card_id: 'fool', text: 'New Beginnings' }];
    useTarotStore.getState().setInterpretations(mockInterps, 'reading-123', 'Overall Good');
    
    const state = useTarotStore.getState();
    expect(state.interpretations).toEqual(mockInterps);
    expect(state.readingId).toBe('reading-123');
    expect(state.overallInterpretation).toBe('Overall Good');
  });
});
