import json
import os
import shutil
import re
from pathlib import Path
import urllib.request

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
TAROT_DATA_TXT = BASE_DIR / "tarot_data.txt"
BACKEND_CARDS_PY = BASE_DIR / "backend/app/data/tarot_cards.py"
I18N_JSON = BASE_DIR / "backend/app/data/i18n/messages.json"
FRONTEND_IMAGES_DIR = BASE_DIR / "frontend/public/cards"

# Ensure directories exist
FRONTEND_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def download_image(url, filename):
    """Download image to frontend public directory."""
    target_path = FRONTEND_IMAGES_DIR / filename
    if target_path.exists():
        print(f"Skipping {filename}, already exists.")
        return
    
    try:
        print(f"Downloading {url} to {filename}...")
        # Use a proper User-Agent to avoid 403s
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def process_tarot_data():
    if not TAROT_DATA_TXT.exists():
        print("tarot_data.txt not found.")
        return

    # Load existing cards to map IDs
    # Since we can't import python file easily here without app context, 
    # we will parse it or just rely on the order/names in txt matching our knowledge.
    # The txt file has lines like: "url chinese_name"
    # The URL contains the English name slug (e.g. The_Fool).
    
    # We will build a new data structure.
    
    new_cards_data = []
    i18n_updates = {"Cards": {}}
    
    with open(TAROT_DATA_TXT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    card_index = 0
    
    # Pre-defined mapping for IDs based on order or name analysis
    # Major Arcana (0-21)
    # Wands (w1-w10, wp, wk, wq, wk2) -> Knight is usually Knight, King is King.
    # The txt seems to have King at the end.
    
    # Let's parse line by line
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(" ")
        if len(parts) < 2:
            continue
            
        url = parts[0]
        name_zh = parts[1]
        
        # Extract English name from URL
        # e.g. .../tarot/The_Fool.webp -> The Fool
        filename = url.split("/")[-1]
        name_slug = filename.replace(".webp", "")
        name_en = name_slug.replace("_", " ")
        
        # Determine ID (Simplistic approach based on known order in txt file)
        # Major: 0-21 (22 cards)
        # Wands: 22-35 (14 cards)
        # Cups: 36-49
        # Swords: 50-63
        # Pentacles: 64-77
        # Back: 78+
        
        card_id = ""
        
        if card_index < 22:
            card_id = str(card_index) # 0..21
        elif 22 <= card_index < 36: # Wands
            idx = card_index - 22
            # Order in txt: Ace, 2-10, Page, Knight, Queen, King
            if idx == 0: card_id = "w1"
            elif idx < 10: card_id = f"w{idx+1}"
            elif idx == 10: card_id = "wp" # Page
            elif idx == 11: card_id = "wk" # Knight
            elif idx == 12: card_id = "wq" # Queen
            elif idx == 13: card_id = "wk2" # King
        elif 36 <= card_index < 50: # Cups
            idx = card_index - 36
            if idx == 0: card_id = "c1"
            elif idx < 10: card_id = f"c{idx+1}"
            elif idx == 10: card_id = "cp"
            elif idx == 11: card_id = "ck"
            elif idx == 12: card_id = "cq"
            elif idx == 13: card_id = "ck2"
        elif 50 <= card_index < 64: # Swords
            idx = card_index - 50
            if idx == 0: card_id = "s1"
            elif idx < 10: card_id = f"s{idx+1}"
            elif idx == 10: card_id = "sp"
            elif idx == 11: card_id = "sk"
            elif idx == 12: card_id = "sq"
            elif idx == 13: card_id = "sk2"
        elif 64 <= card_index < 78: # Pentacles
            idx = card_index - 64
            if idx == 0: card_id = "p1"
            elif idx < 10: card_id = f"p{idx+1}"
            elif idx == 10: card_id = "pp"
            elif idx == 11: card_id = "pk"
            elif idx == 12: card_id = "pq"
            elif idx == 13: card_id = "pk2"
        else:
            # Back or extra
            if "back" in name_slug or "card_back" in name_slug:
                download_image(url, "card_back.webp")
                continue
        
        # Download image
        local_filename = f"{card_id}.webp"
        download_image(url, local_filename)
        
        # Add to i18n
        i18n_key = f"card_{card_id}"
        i18n_updates["Cards"][i18n_key] = {
            "en": name_en,
            "zh": name_zh
        }
        
        # Add to card data
        new_cards_data.append({
            "id": card_id,
            "name_key": i18n_key, # Reference to i18n
            "image": f"/cards/{local_filename}"
        })
        
        card_index += 1

    # Update messages.json
    with open(I18N_JSON, "r", encoding="utf-8") as f:
        current_i18n = json.load(f)
    
    current_i18n.update(i18n_updates)
    
    with open(I18N_JSON, "w", encoding="utf-8") as f:
        json.dump(current_i18n, f, indent=2, ensure_ascii=False)
        
    print("Updated messages.json")

    # Generate new tarot_cards.py content
    py_content = '"""Tarot card data."""\n\n'
    py_content += 'TAROT_CARDS = [\n'
    for card in new_cards_data:
        py_content += f'    {json.dumps(card, ensure_ascii=False)},\n'
    py_content += ']\n\n'
    py_content += 'def get_card_by_id(card_id: str) -> dict | None:\n'
    py_content += '    """Get a tarot card by its ID."""\n'
    py_content += '    for card in TAROT_CARDS:\n'
    py_content += '        if card["id"] == card_id:\n'
    py_content += '            return card\n'
    py_content += '    return None\n'

    with open(BACKEND_CARDS_PY, "w", encoding="utf-8") as f:
        f.write(py_content)
        
    print("Updated tarot_cards.py")

if __name__ == "__main__":
    process_tarot_data()
