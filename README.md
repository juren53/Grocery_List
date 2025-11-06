# Grocery List Organizer

<sub>Version 2.1.4 | Updated: November 6, 2025</sub>

A smart Python-based grocery list organizer that automatically sorts shopping items by store layout (walking order). Simply paste an unorganized list from the clipboard, and get back a neatly organized checklist grouped by store sections.

## ✨ Key Features

- **📋 Clipboard Integration** - Reads unorganized lists directly from clipboard
- **🗂️ Intelligent Categorization** - Automatically sorts items by store sections using keyword matching
- **🧠 Interactive Learning** - Prompts for uncategorized items and learns from the choices
- **📝 Persistent Keywords** - Learns new keywords automatically for better future categorization
- **🔧 Configurable Sections** - Customizable store layout via JSON configuration files
- **✅ Checklist Output** - Generates formatted checklists with checkboxes
- **🏪 Store-Optimized Walking Order** - Items organized in the sequence you encounter them in-store

## 🚀 Quick Start

1. Copy an unorganized shopping list to clipboard
2. Run the script:
   ```bash
   python3 grocery-list.py
   ```
3. If there are unsorted items, categorize them interactively (optional)
4. View the organized list in the terminal and in `shopping_checklist.txt`

## 📂 Project Structure

### Core Application
- **`grocery-list.py`** - Main application (v2.1.4)
- **`grocery-list`** - Shell launcher script

### Configuration Files
- **`sections.json`** - Store sections in walking order
- **`keywords.json`** - Keywords for categorizing items into sections

### Utilities
- **`section_editor.py`** - GUI tool for managing sections with drag-and-drop reordering

### Output
- **`shopping_checklist.txt`** - Generated organized shopping list with checkboxes

### Documentation
- **`NAMING_GUIDE.md`** - Best practices for naming items (corn, tea examples)
- **`GROCERY_LIST_IMPROVEMENTS.md`** - Historical design notes and future plans
- **`Grocery List Organizer Multi-Store Adaptation Strategy-2.md`** - Multi-store strategy documentation

### Archive
- **`archive/`** - Previous versions for reference

## 🎯 How It Works

1. **Input**: Reads shopping list from clipboard (or uses fallback demo list)
2. **Matching**: Scores each item against keywords using word-boundary regex matching
3. **Categorization**: Assigns items to sections based on highest keyword scores
4. **Learning**: Interactively categorizes unsorted items and saves new keywords
5. **Output**: Displays organized list and saves checklist to file

## 📋 Example

**Input (unorganized):**
```
bananas
milk
chicken breast
bread
frozen corn
```

**Output (organized by walking order):**
```
=== Grocery List (Walking Order) === v2.1.4
Generated: Thursday, November 06, 2025 at 06:45 AM

Produce / Fresh Fruits & Vegetables:
  • bananas

Meat & Seafood:
  • chicken breast

Dairy / Refrigerated:
  • milk

Frozen Foods:
  • frozen corn

Bakery:
  • bread
```

## 💡 Pro Tips

- **Be specific with item names** - "frozen corn" vs "corn on the cob" vs "popcorn" each go to different sections
- **Include descriptors** - "green tea" categorizes better than just "tea"
- **Add new keywords** - When prompted, add keywords to improve future runs
- **Check the naming guide** - See `NAMING_GUIDE.md` for detailed examples

## 🛠️ Requirements

- **Python 3.x**
- **pyperclip** - For clipboard integration
  ```bash
  pip install pyperclip
  ```

## 📖 Configuration

### Editing Store Sections
Use the GUI section editor:
```bash
python3 section_editor.py
```

Or manually edit `sections.json` to customize the store's walking order.

### Adding Keywords
Keywords are automatically added when you categorize items interactively, or you can manually edit `keywords.json`.

## 📜 Version History

- **v2.1.4** (2025-11-06) - Added version display in output, created naming guide
- **v2.1.3** (2025-11-05) - Added section_editor.py GUI utility
- **v2.1.1** (2025-11-05) - Interactive categorization with automatic keyword learning
- **v2.0.0** (2025-11-04) - Refactored to use external JSON configuration files
- **v1.0.0** (2024-10-07) - Initial version with hardcoded sections and keywords

## 👤 Author

Jim U'Ren (juren53)

## 📄 License

Open source - feel free to use and modify as needed.
