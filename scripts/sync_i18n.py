import json
import os
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_I18N_PATH = BASE_DIR / "backend/app/data/i18n/messages.json"
FRONTEND_MESSAGES_DIR = BASE_DIR / "frontend/messages"

def sync_i18n():
    if not BACKEND_I18N_PATH.exists():
        print(f"Error: Source file not found at {BACKEND_I18N_PATH}")
        sys.exit(1)

    print(f"Reading from {BACKEND_I18N_PATH}...")
    with open(BACKEND_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Initialize language dictionaries
    languages = ["en", "zh"]
    outputs = {lang: {} for lang in languages}

    def process_node(node, target_dicts):
        """
        Recursively process the JSON tree.
        target_dicts is a dictionary mapping lang code to the current level dictionary for that lang.
        """
        for key, value in node.items():
            # Check if value is a leaf node (translation object)
            # A leaf node in our schema is a dict with keys matching our languages
            if isinstance(value, dict) and all(lang in value for lang in languages):
                # It's a leaf, assign values to respective language dicts
                for lang in languages:
                    target_dicts[lang][key] = value[lang]
            elif isinstance(value, dict):
                # It's a nested category (e.g., "Index", "Auth")
                # Create sub-dictionaries for each language
                sub_target_dicts = {}
                for lang in languages:
                    target_dicts[lang][key] = {}
                    sub_target_dicts[lang] = target_dicts[lang][key]
                
                # Recurse
                process_node(value, sub_target_dicts)
            else:
                print(f"Warning: Unexpected structure at key '{key}'. Skipping.")

    process_node(data, outputs)

    # Ensure frontend directory exists
    FRONTEND_MESSAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Write output files
    for lang, content in outputs.items():
        output_path = FRONTEND_MESSAGES_DIR / f"{lang}.json"
        print(f"Writing {lang} translations to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
    
    print("Synchronization complete!")

if __name__ == "__main__":
    sync_i18n()
