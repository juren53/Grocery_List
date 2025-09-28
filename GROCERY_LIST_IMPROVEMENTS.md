# Improving grocery-list.py — Plan and Design Notes

Last updated: 2025-09-27 4am

## Overview of current workflow
- Copy a raw, unsorted list to the system clipboard
- Script reads from clipboard, scores items using hard-coded substrings, and prints/saves a checklist
- Outliers often fall into an "Unsorted / New Items" bucket

## Pain points
- Rules are brittle (substring-only, no typos handling, brand/phrasing noise)
- No input normalization, so irrelevant text hurts matching
- No learning loop — the same outliers recur week to week
- Categories and walking order are hard-coded in code
- Clipboard is input-only; you still manually copy output elsewhere

## Goals
- Reduce outliers dramatically via normalization + fuzzy matching
- Learn from manual fixes so future runs improve automatically
- Make categories/order editable without code changes
- Keep the process fast: paste → run → paste (clipboard round-trip)

---

## Quick wins (minimal code changes)
1) Normalize inputs
   - Lowercase
   - Strip punctuation and collapse whitespace
   - Remove noise phrases (e.g., "friday freebie", "free price chopper", "see email", "for eva", "pack", "pk", "small")
   - Simple plural→singular (chips→chip, muffins→muffin)
   - Synonyms/aliases (cherrios→cheerios, oj→orange juice)

2) Weighted scoring
   - Phrase hit: +3 (e.g., "egg salad")
   - Token hit: +1 (e.g., "egg")
   - Fuzzy token hit: +0.5 (to catch light typos)

3) Fuzzy matching
   - Use difflib.SequenceMatcher for a lightweight dependency-free start
   - Phrase threshold ~0.85; token threshold ~0.90
   - Optionally upgrade to rapidfuzz for speed and quality later

4) Deduplicate and tidy sections
   - Use sets to dedupe, then sort items within each section
   - Keep "Unsorted / New Items" visible (top or bottom consistently)

5) Clipboard out
   - After generating the formatted list, copy it back to the clipboard as well as write to file

---

## Configuration file (externalize categories and order)
Move categories, keywords, walking order, stopwords, and synonyms into a YAML file (e.g., `config/categories.yaml`).

- Editable without touching code
- Easy to extend and share
- Supports multi-store profiles later (per-store order and categories)

Suggested YAML structure:

```yaml
order:
  - Produce
  - Deli / Prepared Foods
  - Bakery
  - Juice & Canned Fruit
  - Cereal & Breakfast
  - Snacks
  - Dairy / Refrigerated
  - Beverages / Water

stopwords:
  - friday freebie
  - free price chopper
  - see email
  - for eva
  - for
  - pk
  - pack
  - small

synonyms:
  cheerios: [cherrios]
  orange juice: [oj]

weights:
  phrase: 3
  token: 1
  fuzzy_token: 0.5

categories:
  Produce:
    phrases: ["dole salad"]
    tokens: ["banana", "lettuce", "tomato"]
  Deli / Prepared Foods:
    phrases: ["egg salad", "tuna salad", "cole slaw"]
    tokens: ["bologna"]
  Bakery:
    tokens: ["muffin", "bread", "roll"]
  Juice & Canned Fruit:
    phrases: ["apple sauce"]
    tokens: ["cranberry"]
  Cereal & Breakfast:
    tokens: ["wheaties", "nutra", "cheerios"]
  Snacks:
    tokens: ["cracker", "chip"]
  Dairy / Refrigerated:
    phrases: ["orange juice"]
    tokens: ["milk", "cheese", "egg", "yogurt"]
  Beverages / Water:
    tokens: ["water", "coke", "lemonade", "soda", "cola", "tea"]
```

Multi-store idea (later): have `stores/price_chopper.yaml`, `stores/walmart.yaml` with their own `order`, `categories`, `stopwords`, etc., and select with `--store price_chopper`.

---

## Learning loop for outliers
Two ergonomic options:

1) Interactive (default opt-in with `--interactive`)
   - When an item lands in "Unsorted", prompt: "Assign to which category?"
   - Optionally ask for a phrase or token to persist (defaults to the normalized item)
   - Append to `categories.yaml` automatically (backup before writing)

2) Offline triage
   - Log unknowns to `data/new_items.tsv` with timestamp and raw/normalized text
   - Add a `--train` mode that walks through pending items and updates `categories.yaml`

---

## Fuzzy matching details
- Try exact phrase matches first (highest weight)
- Then fuzzy phrase match (0.85–0.90 threshold)
- Then token presence / fuzzy token
- If scores tie, use a stable priority: earlier categories in `order` win

Optional upgrade: use `rapidfuzz` for better speed and token-based scorers when lists grow larger.

---

## CLI ergonomics
Add argparse flags to fit different workflows:

- Input:
  - `--from-clipboard` (default)
  - `--from-file <path>`
  - `--from-stdin`
- Output:
  - `--to-clipboard` (default)
  - `--to-file <path>` (default `shopping_checklist.txt`)
  - `--print`
- Behavior:
  - `--interactive` / `--no-interactive`
  - `--store <name>` (for multi-store profiles later)
  - `--dedupe` (default on)
  - `--aggregate` (combine duplicates and parse simple quantities like "24 pk")
  - `--show-suggestions <N>` (for uncertain classification)

Logging:
- Append outliers to `data/new_items.tsv` for later review

---

## Optional ML assist (lightweight)
- Keep `data/history.csv` of normalized items and final categories
- Periodically train a TF-IDF + Logistic Regression (or Naive Bayes) classifier
- At runtime, if ML confidence ≥ threshold (e.g., 0.75), accept; otherwise mark Unsorted with top-3 suggestions
- Persist model as `models/grocery_model.joblib`

This is strictly additive; the rule-based system remains the primary logic and source of truth.

---

## Implementation sketch (pseudocode)

Normalization:

```python
import re

def normalize(text: str, stopwords: set[str], synonyms: dict[str, list[str]]) -> str:
    t = text.lower()
    # apply synonyms (map variants to a canonical form)
    for canon, variants in synonyms.items():
        for v in variants:
            t = t.replace(v, canon)
    # remove noise phrases
    for sw in stopwords:
        t = t.replace(sw, " ")
    # keep digits and a few separators
    t = re.sub(r"[^a-z0-9\s/&-]", " ", t)
    # simple plural→singular
    t = re.sub(r"\b(\w+?)s\b", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
```

Scoring with fuzzy:

```python
from difflib import SequenceMatcher

def fuzzy_contains(haystack: str, needle: str, threshold: float = 0.85) -> bool:
    if needle in haystack:
        return True
    return SequenceMatcher(None, haystack, needle).ratio() >= threshold

def score_item(norm_item: str, rule: dict, weights: dict) -> float:
    score = 0.0
    for p in rule.get("phrases", []):
        if fuzzy_contains(norm_item, p, threshold=0.87):
            score += weights.get("phrase", 3)
    tokens = norm_item.split()
    for tok in rule.get("tokens", []):
        if tok in tokens:
            score += weights.get("token", 1)
        elif fuzzy_contains(norm_item, tok, threshold=0.9):
            score += weights.get("fuzzy_token", 0.5)
    return score
```

Learning (interactive):

```python
def learn_mapping(raw_item: str, categories: list[str]) -> tuple[str, str] | None:
    print(f"Unsorted: {raw_item}")
    for i, c in enumerate(categories, 1):
        print(f"  {i}) {c}")
    print("  0) Skip")
    try:
        choice = int(input("Assign to: "))
    except ValueError:
        return None
    if choice <= 0 or choice > len(categories):
        return None
    category = categories[choice - 1]
    phrase = input("Add a phrase to learn (Enter to use full item): ").strip() or raw_item
    return category, phrase
```

---

## Migration plan
- Phase 1 (today):
  - Add normalization, weighted scoring, dedupe/sort, and clipboard out
- Phase 2:
  - Introduce `config/categories.yaml`; retain in-code defaults as fallback
- Phase 3:
  - Add interactive learning that updates the YAML (with automatic backups)
- Phase 4:
  - Fuzzy matching thresholds and optional `rapidfuzz`
- Phase 5 (optional):
  - ML classifier gated by confidence threshold; keep rules authoritative

---

## Testing strategy
- Unit tests for `normalize()` with realistic noisy strings
- Unit tests for scoring: phrase vs token precedence, fuzzy behavior, tie-breaking
- Golden file tests: given a sample input list, expect a fixed sectioned output

---

## Dependencies
- Baseline: standard library + `pyperclip`
- Optional:
  - `pyyaml` (config)
  - `rapidfuzz` (fuzzy matching performance/quality)
  - `scikit-learn`, `joblib` (optional ML)

Example dev requirements:

```
pyyaml
rapidfuzz
scikit-learn
joblib
```

---

## Appendix A: Example `categories.yaml`

See the sample in the Configuration section; copy it to `config/categories.yaml` and tweak for your store.

---

## Appendix B: Example commands (future flags)
- Read from clipboard, write file, interactive learning:
  - `python grocery-list.py --from-clipboard --to-file shopping_checklist.txt --interactive`
- Pipe from a file, copy sorted result to clipboard:
  - `cat raw_list.txt | python grocery-list.py --from-stdin --to-clipboard`

---

## Why this reduces outliers
- Normalization strips non-signal noise (freebie phrases, names, brand fluff)
- Fuzzy matching catches typos like "cherrios"
- Learning ensures once you classify an outlier, you won’t see it again
- External config lets you adjust aisles and order without code edits

---

## Next steps
If/when you want, implement Phase 1 and we can iterate. Once normalization and weighted scoring are in, we’ll already see a noticeable drop in Unsorted items.
