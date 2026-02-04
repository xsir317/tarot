"""Tarot card data."""

TAROT_CARDS: list[dict[str, str]] = [
    # Major Arcana
    {"id": "0", "name": "愚者", "name_en": "The Fool", "name_zh": "愚者"},
    {"id": "1", "name": "魔术师", "name_en": "The Magician", "name_zh": "魔术师"},
    {"id": "2", "name": "女祭司", "name_en": "The High Priestess", "name_zh": "女祭司"},
    {"id": "3", "name": "女皇", "name_en": "The Empress", "name_zh": "女皇"},
    {"id": "4", "name": "皇帝", "name_en": "The Emperor", "name_zh": "皇帝"},
    {"id": "5", "name": "教皇", "name_en": "The Hierophant", "name_zh": "教皇"},
    {"id": "6", "name": "恋人", "name_en": "The Lovers", "name_zh": "恋人"},
    {"id": "7", "name": "战车", "name_en": "The Chariot", "name_zh": "战车"},
    {"id": "8", "name": "力量", "name_en": "Strength", "name_zh": "力量"},
    {"id": "9", "name": "隐士", "name_en": "The Hermit", "name_zh": "隐士"},
    {"id": "10", "name": "命运之轮", "name_en": "Wheel of Fortune", "name_zh": "命运之轮"},
    {"id": "11", "name": "正义", "name_en": "Justice", "name_zh": "正义"},
    {"id": "12", "name": "倒吊人", "name_en": "The Hanged Man", "name_zh": "倒吊人"},
    {"id": "13", "name": "死神", "name_en": "Death", "name_zh": "死神"},
    {"id": "14", "name": "节制", "name_en": "Temperance", "name_zh": "节制"},
    {"id": "15", "name": "恶魔", "name_en": "The Devil", "name_zh": "恶魔"},
    {"id": "16", "name": "高塔", "name_en": "The Tower", "name_zh": "高塔"},
    {"id": "17", "name": "星星", "name_en": "The Star", "name_zh": "星星"},
    {"id": "18", "name": "月亮", "name_en": "The Moon", "name_zh": "月亮"},
    {"id": "19", "name": "太阳", "name_en": "The Sun", "name_zh": "太阳"},
    {"id": "20", "name": "审判", "name_en": "Judgement", "name_zh": "审判"},
    {"id": "21", "name": "世界", "name_en": "The World", "name_zh": "世界"},
    # Minor Arcana - Wands
    {"id": "w1", "name": "权杖首牌", "name_en": "Ace of Wands", "name_zh": "权杖首牌"},
    {"id": "w2", "name": "权杖二", "name_en": "Two of Wands", "name_zh": "权杖二"},
    {"id": "w3", "name": "权杖三", "name_en": "Three of Wands", "name_zh": "权杖三"},
    {"id": "w4", "name": "权杖四", "name_en": "Four of Wands", "name_zh": "权杖四"},
    {"id": "w5", "name": "权杖五", "name_en": "Five of Wands", "name_zh": "权杖五"},
    {"id": "w6", "name": "权杖六", "name_en": "Six of Wands", "name_zh": "权杖六"},
    {"id": "w7", "name": "权杖七", "name_en": "Seven of Wands", "name_zh": "权杖七"},
    {"id": "w8", "name": "权杖八", "name_en": "Eight of Wands", "name_zh": "权杖八"},
    {"id": "w9", "name": "权杖九", "name_en": "Nine of Wands", "name_zh": "权杖九"},
    {"id": "w10", "name": "权杖十", "name_en": "Ten of Wands", "name_zh": "权杖十"},
    {"id": "wp", "name": "权杖侍从", "name_en": "Page of Wands", "name_zh": "权杖侍从"},
    {"id": "wk", "name": "权杖骑士", "name_en": "Knight of Wands", "name_zh": "权杖骑士"},
    {"id": "wq", "name": "权杖王后", "name_en": "Queen of Wands", "name_zh": "权杖王后"},
    {"id": "wk2", "name": "权杖国王", "name_en": "King of Wands", "name_zh": "权杖国王"},
    # Minor Arcana - Cups
    {"id": "c1", "name": "圣杯首牌", "name_en": "Ace of Cups", "name_zh": "圣杯首牌"},
    {"id": "c2", "name": "圣杯二", "name_en": "Two of Cups", "name_zh": "圣杯二"},
    {"id": "c3", "name": "圣杯三", "name_en": "Three of Cups", "name_zh": "圣杯三"},
    {"id": "c4", "name": "圣杯四", "name_en": "Four of Cups", "name_zh": "圣杯四"},
    {"id": "c5", "name": "圣杯五", "name_en": "Five of Cups", "name_zh": "圣杯五"},
    {"id": "c6", "name": "圣杯六", "name_en": "Six of Cups", "name_zh": "圣杯六"},
    {"id": "c7", "name": "圣杯七", "name_en": "Seven of Cups", "name_zh": "圣杯七"},
    {"id": "c8", "name": "圣杯八", "name_en": "Eight of Cups", "name_zh": "圣杯八"},
    {"id": "c9", "name": "圣杯九", "name_en": "Nine of Cups", "name_zh": "圣杯九"},
    {"id": "c10", "name": "圣杯十", "name_en": "Ten of Cups", "name_zh": "圣杯十"},
    {"id": "cp", "name": "圣杯侍从", "name_en": "Page of Cups", "name_zh": "圣杯侍从"},
    {"id": "ck", "name": "圣杯骑士", "name_en": "Knight of Cups", "name_zh": "圣杯骑士"},
    {"id": "cq", "name": "圣杯王后", "name_en": "Queen of Cups", "name_zh": "圣杯王后"},
    {"id": "ck2", "name": "圣杯国王", "name_en": "King of Cups", "name_zh": "圣杯国王"},
    # Minor Arcana - Swords
    {"id": "s1", "name": "宝剑首牌", "name_en": "Ace of Swords", "name_zh": "宝剑首牌"},
    {"id": "s2", "name": "宝剑二", "name_en": "Two of Swords", "name_zh": "宝剑二"},
    {"id": "s3", "name": "宝剑三", "name_en": "Three of Swords", "name_zh": "宝剑三"},
    {"id": "s4", "name": "宝剑四", "name_en": "Four of Swords", "name_zh": "宝剑四"},
    {"id": "s5", "name": "宝剑五", "name_en": "Five of Swords", "name_zh": "宝剑五"},
    {"id": "s6", "name": "宝剑六", "name_en": "Six of Swords", "name_zh": "宝剑六"},
    {"id": "s7", "name": "宝剑七", "name_en": "Seven of Swords", "name_zh": "宝剑七"},
    {"id": "s8", "name": "宝剑八", "name_en": "Eight of Swords", "name_zh": "宝剑八"},
    {"id": "s9", "name": "宝剑九", "name_en": "Nine of Swords", "name_zh": "宝剑九"},
    {"id": "s10", "name": "宝剑十", "name_en": "Ten of Swords", "name_zh": "宝剑十"},
    {"id": "sp", "name": "宝剑侍从", "name_en": "Page of Swords", "name_zh": "宝剑侍从"},
    {"id": "sk", "name": "宝剑骑士", "name_en": "Knight of Swords", "name_zh": "宝剑骑士"},
    {"id": "sq", "name": "宝剑王后", "name_en": "Queen of Swords", "name_zh": "宝剑王后"},
    {"id": "sk2", "name": "宝剑国王", "name_en": "King of Swords", "name_zh": "宝剑国王"},
    # Minor Arcana - Pentacles
    {"id": "p1", "name": "星币首牌", "name_en": "Ace of Pentacles", "name_zh": "星币首牌"},
    {"id": "p2", "name": "星币二", "name_en": "Two of Pentacles", "name_zh": "星币二"},
    {"id": "p3", "name": "星币三", "name_en": "Three of Pentacles", "name_zh": "星币三"},
    {"id": "p4", "name": "星币四", "name_en": "Four of Pentacles", "name_zh": "星币四"},
    {"id": "p5", "name": "星币五", "name_en": "Five of Pentacles", "name_zh": "星币五"},
    {"id": "p6", "name": "星币六", "name_en": "Six of Pentacles", "name_zh": "星币六"},
    {"id": "p7", "name": "星币七", "name_en": "Seven of Pentacles", "name_zh": "星币七"},
    {"id": "p8", "name": "星币八", "name_en": "Eight of Pentacles", "name_zh": "星币八"},
    {"id": "p9", "name": "星币九", "name_en": "Nine of Pentacles", "name_zh": "星币九"},
    {"id": "p10", "name": "星币十", "name_en": "Ten of Pentacles", "name_zh": "星币十"},
    {"id": "pp", "name": "星币侍从", "name_en": "Page of Pentacles", "name_zh": "星币侍从"},
    {"id": "pk", "name": "星币骑士", "name_en": "Knight of Pentacles", "name_zh": "星币骑士"},
    {"id": "pq", "name": "星币王后", "name_en": "Queen of Pentacles", "name_zh": "星币王后"},
    {"id": "pk2", "name": "星币国王", "name_en": "King of Pentacles", "name_zh": "星币国王"},
]


def get_card_by_id(card_id: str) -> dict[str, str] | None:
    """Get a tarot card by its ID.

    Args:
        card_id: The card ID

    Returns:
        Card data dict or None if not found
    """
    for card in TAROT_CARDS:
        if card["id"] == card_id:
            return card
    return None
