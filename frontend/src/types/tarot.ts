export interface Card {
  id: string
  name: string
  nameEn: string
  suit: 'major' | 'minor'
  number?: number
  meaning: {
    upright: string
    reversed: string
  }
  imageUrl?: string
}

export type CardPosition = 'past' | 'present' | 'future'
