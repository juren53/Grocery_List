# grocery_list_sorter.py

shopping_list = [
    "bananas",
    "egg salad",
    "1 Dole salad",
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
    "Cherrios"  # new test item
]

# Store sections in walking order
sections = {
    "Produce": [],
    "Deli / Prepared Foods": [],
    "Bakery": [],
    "Cereal & Breakfast": [],
    "Snacks": [],
    "Dairy / Refrigerated": [],
    "Beverages / Water": []
}

# Keywords per section
keywords = {
    "Produce": ["banana", "salad"],
    "Deli / Prepared Foods": ["egg salad", "tuna", "cole slaw", "bologna"],
    "Bakery": ["muffin"],
    "Cereal & Breakfast": ["wheaties", "nutra", "apple sauce", "cheerios", "cherrios"],
    "Snacks": ["cracker", "chip"],
    "Dairy / Refrigerated": ["milk", "juice", "egg bites"],
    "Beverages / Water": ["water"]
}

# Categorization logic: score matches for each section
for item in shopping_list:
    lower_item = item.lower()
    scores = {section: 0 for section in sections}

    for section, keys in keywords.items():
        for k in keys:
            if k in lower_item:
                scores[section] += 1

    # Pick the section with the highest score
    best_section = max(scores, key=scores.get)

    # If no keywords matched, fallback to Deli
    if scores[best_section] == 0:
        best_section = "Deli / Prepared Foods"

    sections[best_section].append(item)

# Print neatly to console
print("\n=== Grocery List (Walking Order) ===\n")
for section, items in sections.items():
    if items:
        print(f"{section}:")
        for i in items:
            print(f"  • {i}")
        print()

# Save to a printable checklist file
with open("shopping_checklist.txt", "w") as f:
    f.write("=== Grocery Checklist ===\n\n")
    for section, items in sections.items():
        if items:
            f.write(f"{section}:\n")
            for i in items:
                f.write(f"• [ ] {i}\n")
            f.write("\n")

print("✅ Checklist saved to shopping_checklist.txt")
# grocery_list_sorter.py

shopping_list = [
    "bananas",
    "egg salad",
    "1 Dole salad",
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
    "Cherrios"  # new test item
]

# Store sections in walking order
sections = {
    "Produce": [],
    "Deli / Prepared Foods": [],
    "Bakery": [],
    "Cereal & Breakfast": [],
    "Snacks": [],
    "Dairy / Refrigerated": [],
    "Beverages / Water": []
}

# Keywords per section
keywords = {
    "Produce": ["banana", "salad"],
    "Deli / Prepared Foods": ["egg salad", "tuna", "cole slaw", "bologna"],
    "Bakery": ["muffin"],
    "Cereal & Breakfast": ["wheaties", "nutra", "apple sauce", "cheerios", "cherrios"],
    "Snacks": ["cracker", "chip"],
    "Dairy / Refrigerated": ["milk", "juice", "egg bites"],
    "Beverages / Water": ["water"]
}

# Categorization logic: score matches for each section
for item in shopping_list:
    lower_item = item.lower()
    scores = {section: 0 for section in sections}

    for section, keys in keywords.items():
        for k in keys:
            if k in lower_item:
                scores[section] += 1

    # Pick the section with the highest score
    best_section = max(scores, key=scores.get)

    # If no keywords matched, fallback to Deli
    if scores[best_section] == 0:
        best_section = "Deli / Prepared Foods"

    sections[best_section].append(item)

# Print neatly to console
print("\n=== Grocery List (Walking Order) ===\n")
for section, items in sections.items():
    if items:
        print(f"{section}:")
        for i in items:
            print(f"  • {i}")
        print()

# Save to a printable checklist file
with open("shopping_checklist.txt", "w") as f:
    f.write("=== Grocery Checklist ===\n\n")
    for section, items in sections.items():
        if items:
            f.write(f"{section}:\n")
            for i in items:
                f.write(f"• [ ] {i}\n")
            f.write("\n")

print("✅ Checklist saved to shopping_checklist.txt")

