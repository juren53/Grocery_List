# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

The Grocery List Manager is a Python application that organizes shopping lists by store sections. It reads unstructured grocery items from the clipboard, categorizes them using keyword matching, and generates a walking-order checklist for efficient shopping.

**Core Workflow:**
1. Copy raw shopping list to clipboard
2. Run `grocery-list.py` which reads from clipboard
3. Items are categorized by matching against keywords in `keywords.json`
4. Interactive prompts handle uncategorized items with learning capability
5. Outputs organized checklist to console and `shopping_checklist.txt`

## Key Commands

### Running the Application
```bash
python grocery-list.py
```

The main script requires Python 3.x and the `pyperclip` library. It will automatically fall back to a demo list if the clipboard is empty.

### Running Archived Versions
Previous iterations are stored in the `archive/` directory:
```bash
python archive/grocery-list-2.py
python archive/grocery-list-3.py
python archive/grocery-list-4.py
python archive/grocery-list-5.py
```

### Testing
There is currently no formal test suite. Manual testing workflow:
1. Copy a sample list to clipboard
2. Run the script
3. Verify categorization in console output
4. Check `shopping_checklist.txt` for proper formatting

## Architecture & Structure

### Configuration-Driven Design

The application is externalized into data files to avoid hard-coding:

- **`sections.json`**: Ordered list of store sections (walking order)
- **`keywords.json`**: Mapping of sections to categorization keywords
- **`shopping_checklist.txt`**: Generated output file with checkboxes

### Categorization Algorithm

The core categorization logic (lines 75-92 in `grocery-list.py`) uses a simple scoring system:

1. Each item is lowercased and compared against all keywords
2. Score accumulates +1 for each keyword match (substring match)
3. Item is assigned to the section with the highest score
4. Items with score of 0 go to "Unsorted / New Items"

**Important**: This is substring matching, not token-based. "egg" will match "egg salad", "eggplant", etc.

### Interactive Learning System

When uncategorized items are found (lines 94-152):

1. User is prompted to assign each unsorted item to a section
2. User can optionally add the item as a keyword for future runs
3. New keywords are automatically appended to `keywords.json`
4. The system "learns" from manual categorization

**File Mutation**: The script writes to `keywords.json` during interactive sessions. Always ensure this file is backed up or in version control.

### Version History

The codebase shows iterative development:
- **v1.0.0**: Initial version with hard-coded sections/keywords
- **v2.0.0**: Refactored to use external JSON configuration
- **v2.1.1** (current): Added interactive categorization with keyword learning

Previous versions are archived in `archive/` for reference but are not actively maintained.

## Development Guidelines

### Modifying Categories

To add/remove store sections:
1. Edit `sections.json` (order matters - represents walking path)
2. Add corresponding entry in `keywords.json`
3. Test with sample data

### Extending Keyword Matching

Current system limitations (see `GROCERY_LIST_IMPROVEMENTS.md` for planned enhancements):
- No fuzzy matching (typos cause misses)
- No normalization (punctuation, plurals, noise phrases affect matching)
- No weighted scoring (phrase matches treated same as token matches)

When adding keywords:
- Use lowercase only
- Consider common misspellings
- Think about substrings that might cause false positives

### Output Format

The script generates two outputs:
1. **Console**: Human-readable with bullet points
2. **`shopping_checklist.txt`**: Checkbox format `• [ ] item`

Both include timestamp and section headers. Format changes should maintain consistency between outputs.

### Dependencies

- **Required**: `pyperclip` for clipboard access
- **Optional** (planned): `pyyaml`, `rapidfuzz`, `scikit-learn` for future improvements

No `requirements.txt` currently exists. Install dependencies manually:
```bash
pip install pyperclip
```

## Planned Improvements

See `GROCERY_LIST_IMPROVEMENTS.md` for detailed roadmap. Key planned phases:

1. **Normalization**: Strip noise phrases, handle plurals, apply synonyms
2. **Fuzzy Matching**: Use `difflib` or `rapidfuzz` for typo tolerance  
3. **Weighted Scoring**: Phrase matches > token matches > fuzzy matches
4. **YAML Config**: Migrate to `config/categories.yaml` with stopwords and weights
5. **ML Classifier** (optional): Train on history for better auto-categorization

## Important Notes

- **Windows Environment**: This codebase is developed on Windows (PowerShell). Path handling uses Windows conventions.
- **Timezone**: All timestamps use CST (Central Standard Time, UTC-6). Version timestamps should use the format `YYYY-MM-DDTHH:MM:SS-06:00`.
- **No Automation**: The script is run manually per shopping session. No scheduled tasks or daemons.
- **State Persistence**: Only `keywords.json` and `shopping_checklist.txt` maintain state between runs. The application itself is stateless.
- **Clipboard Required**: Primary input is via clipboard using `pyperclip`. Alternative input methods (file, stdin) are planned but not implemented.
