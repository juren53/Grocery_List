#!/usr/bin/python3
# grocery-list.py
# Version: 2.0.0
# Last Updated: 2025-11-04T22:22:53Z
#-----------------------------------------------------------
# Grocery list organizer and sorter by store sections
# Takes shopping list from clipboard and sorts by walking order
#
# Changelog:
# v2.0.0 (2025-11-04) - Refactored to use external JSON files for
#                       sections and keywords configuration
# v1.0.0 (2024-10-07) - Initial version with hardcoded sections
#-----------------------------------------------------------

import pyperclip
import json
from datetime import datetime

# Version information
VERSION = "2.0.0"
LAST_UPDATED = "2025-11-04T22:22:53Z"

print(f"Grocery List Organizer v{VERSION} (Updated: {LAST_UPDATED})\n")

# Try to pull list from clipboard
raw_clipboard = pyperclip.paste().strip()

if raw_clipboard:
    print("📋 Using shopping list from clipboard...\n")
    # Split on newlines to get items
    shopping_list = [line.strip() for line in raw_clipboard.splitlines() if line.strip()]
else:
    print("⚠️ Clipboard empty — using fallback demo list...\n")
    shopping_list = [
        "bananas",
        "golden delicious apple",
        "bartlett pears",
        "egg salad",
        "1 Dole salad",
        "off the bone turkey",
        "Tuna salad",
        "Cole slaw",
        "mini blueberry muffins",
        "Wheaties",
        "Small Oscar Mayer Beef Bologna",
        "Free price Chopper water -24 pk. - see email",
        "cinnamon honey apple sauce for Eva",
        "grilled cheese crackers",
        "1 low sodium Lay's chips",
        "nutra grain breakfast bars",
        "Friday Freebie - Tropicana Orange Juice - see email",
        "egg bites asiato mushroom",
        "milk",
        "Cherrios",
        "Coke",
        "Lemonade",
        "Cranberry Juice",
        "Cottage Cheese",
        "Chocolate Milk"
    ]

# Load sections from JSON file
with open("sections.json", "r") as f:
    section_names = json.load(f)

# Load keywords from JSON file
with open("keywords.json", "r") as f:
    keywords = json.load(f)

# Initialize sections dictionary with empty lists
sections = {section: [] for section in section_names}

# Categorization logic
for item in shopping_list:
    lower_item = item.lower()
    scores = {section: 0 for section in sections}

    for section, keys in keywords.items():
        for k in keys:
            if k in lower_item:
                scores[section] += 1

    best_section = max(scores, key=scores.get)

    if scores[best_section] == 0:
        if "Unsorted / New Items" not in sections:
            sections["Unsorted / New Items"] = []
        best_section = "Unsorted / New Items"

    sections[best_section].append(item)

# Print neatly to console
generated_time = datetime.now()
formatted_time = generated_time.strftime("%A, %B %d, %Y at %I:%M %p")

print(f"\n=== Grocery List (Walking Order) ===\nGenerated: {formatted_time}\n")
for section, items in sections.items():
    if items:
        print(f"{section}:")
        for i in items:
            print(f"  • {i}")
        print()

# Save to checklist file
generated_time = datetime.now()
formatted_time = generated_time.strftime("%A, %B %d, %Y at %I:%M %p")

with open("shopping_checklist.txt", "w") as f:
    f.write("=== Grocery Checklist ===\n")
    f.write(f"Generated: {formatted_time}\n\n")
    for section, items in sections.items():
        if items:
            f.write(f"{section}:\n")
            for i in items:
                f.write(f"• [ ] {i}\n")
            f.write("\n")

print("✅ Checklist saved to shopping_checklist.txt")

