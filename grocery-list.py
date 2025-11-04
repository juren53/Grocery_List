#!/usr/bin/python3
# grocery-list.py
#-----------------------------------------------------------
# Grocery list organizer and sorter by store sections
# Takes shopping list from clipboard and sorts by walking order
# last edited on Mon 07 Oct 2024 02:55:45 PM UTC - initial header
#-----------------------------------------------------------

import pyperclip

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

# Store sections in walking order
sections = {
    "Produce": [],
    "Deli / Prepared Foods": [],
    "Bakery": [],
    "Juice & Canned Fruit": [],
    "Cereal & Breakfast": [],
    "Snacks": [],
    "Dairy / Refrigerated": [],
    "Beverages / Water": []
}

# Keywords per section
keywords = {
    "Produce": ["banana", "dole salad","golden delicious apple","bartlett pears"],
    "Deli / Prepared Foods": ["egg salad", "tuna salad", "chicken salad", "cole slaw", "bologna","off the bone turkey"],
    "Bakery": ["muffin"],
    "Juice & Canned Fruit": ["apple sauce", "cranberry"],
    "Cereal & Breakfast": ["wheaties", "nutra", "cheerios", "cherrios"],
    "Snacks": ["cracker", "chip"],
    "Dairy / Refrigerated": ["milk", "cheese", "orange juice", "egg"],
    "Beverages / Water": ["water", "coke", "lemonade", "soda", "cola", "tea"]
}

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
print("\n=== Grocery List (Walking Order) ===\n")
for section, items in sections.items():
    if items:
        print(f"{section}:")
        for i in items:
            print(f"  • {i}")
        print()

# Save to checklist file
with open("shopping_checklist.txt", "w") as f:
    f.write("=== Grocery Checklist ===\n\n")
    for section, items in sections.items():
        if items:
            f.write(f"{section}:\n")
            for i in items:
                f.write(f"• [ ] {i}\n")
            f.write("\n")

print("✅ Checklist saved to shopping_checklist.txt")

