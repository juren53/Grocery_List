#!/usr/bin/python3
# grocery-list.py
# Version: 2.1.3
# Last Updated: 2025-11-05T16:24:10-06:00
#-----------------------------------------------------------
# Grocery list organizer and sorter by store sections
# Takes shopping list from clipboard and sorts by walking order
#
# Changelog:
# v2.1.3 (2025-11-05) - Added section_editor.py GUI utility for managing
#                       sections.json with drag-and-drop reordering
# v2.1.1 (2025-11-05) - Added interactive categorization for unsorted items
#                       with automatic keyword learning 
# v2.0.0 (2025-11-04) - Refactored to use with external JSON files for
#                       sections and keywords configuration
# v1.0.0 (2024-10-07) - Initial version w hardcoded sections & keywords
#-----------------------------------------------------------

import pyperclip
import json
from datetime import datetime

# Version information
VERSION = "2.1.3"
LAST_UPDATED = "2025-11-05T16:24:10-06:00"

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

# Handle unsorted items interactively
if "Unsorted / New Items" in sections and sections["Unsorted / New Items"]:
    print("\n🤔 Found unsorted items! Let's categorize them...\n")
    
    # Show available sections
    print("Available sections:")
    for i, section in enumerate(section_names, 1):
        print(f"  {i}. {section}")
    print(f"  {len(section_names) + 1}. Skip (keep unsorted)")
    print()
    
    unsorted_items = sections["Unsorted / New Items"].copy()
    sections["Unsorted / New Items"] = []
    new_keywords = {}
    
    for item in unsorted_items:
        print(f"📦 Item: '{item}'")
        while True:
            try:
                choice = input(f"Choose section (1-{len(section_names) + 1}): ").strip()
                if choice == str(len(section_names) + 1):
                    # Skip - keep unsorted
                    sections["Unsorted / New Items"].append(item)
                    break
                elif 1 <= int(choice) <= len(section_names):
                    selected_section = section_names[int(choice) - 1]
                    sections[selected_section].append(item)
                    
                    # Ask if user wants to add this as a keyword
                    add_keyword = input(f"Add '{item}' as keyword? (Y/n): ").strip().lower()
                    if add_keyword == 'y' or add_keyword == 'yes' or add_keyword == '':
                        # Extract main word(s) from item - take first significant word
                        keyword = item.lower().strip()
                        if selected_section not in new_keywords:
                            new_keywords[selected_section] = []
                        new_keywords[selected_section].append(keyword)
                        print(f"✅ Added '{keyword}' to {selected_section} keywords")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(section_names) + 1}")
            except ValueError:
                print(f"Please enter a valid number between 1 and {len(section_names) + 1}")
        print()
    
    # Update keywords.json if new keywords were added
    if new_keywords:
        for section, new_keys in new_keywords.items():
            if section in keywords:
                keywords[section].extend(new_keys)
            else:
                keywords[section] = new_keys
        
        with open("keywords.json", "w") as f:
            json.dump(keywords, f, indent=4)
        print(f"📝 Updated keywords.json with {sum(len(keys) for keys in new_keywords.values())} new keywords")
    
    # Clean up empty unsorted section
    if not sections["Unsorted / New Items"]:
        del sections["Unsorted / New Items"]

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

