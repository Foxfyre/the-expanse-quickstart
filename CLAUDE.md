# Claude Code Instructions

## PDF Processing for Large Documents

### The Problem
When processing PDFs as images, large documents cause `API Error: 413 {"error":{"type":"request_too_large"}}`. The Anthropic API has a ~20-25 MB request size limit, and base64-encoded images inflate size by ~33%.

### The Solution
Extract text from PDFs using PyMuPDF instead of sending page images. Text is much smaller and avoids the size limit entirely.

### Using the Extraction Script

```bash
# Check PDF info without extracting
python scripts/extract_pdf_text.py pdfs/some_file.pdf --info

# Extract to text with automatic chunking (default 40k chars per chunk)
python scripts/extract_pdf_text.py pdfs/some_file.pdf -o pdfs_text

# Extract all PDFs at once
python scripts/extract_pdf_text.py all -o pdfs_text

# Extract specific pages (1-indexed)
python scripts/extract_pdf_text.py pdfs/some_file.pdf -p 5,6,7,8

# Custom chunk size
python scripts/extract_pdf_text.py pdfs/some_file.pdf -o pdfs_text --chunk-size 30000

# Print to stdout (for piping)
python scripts/extract_pdf_text.py pdfs/some_file.pdf --stdout
```

### Output Structure
```
pdfs_text/
└── PDF_Name/
    ├── PDF_Name_page_001.txt    # Individual pages
    ├── PDF_Name_page_002.txt
    ├── ...
    ├── PDF_Name_chunk_01.txt    # API-friendly chunks (~10k tokens each)
    ├── PDF_Name_chunk_02.txt
    ├── ...
    └── PDF_Name_complete.txt    # Full text in one file
```

### Workflow for Extracting Foundry VTT Content

1. **Extract text from PDF:**
   ```bash
   python scripts/extract_pdf_text.py pdfs/NewBook.pdf --info
   python scripts/extract_pdf_text.py pdfs/NewBook.pdf -o pdfs_text
   ```

2. **Read chunks to find relevant content:**
   - Check table of contents (usually early pages)
   - Search for keywords like "talent", "stunt", "equipment"
   ```bash
   grep -l "Talent\|Stunt" pdfs_text/NewBook/*.txt
   ```

3. **Create extraction script** following the pattern in `add_*.py`:
   - Define items with name, cost, description
   - Use `generate_id()` for unique IDs
   - Create folders if needed
   - Check for duplicates before adding

4. **Run and verify:**
   ```bash
   python add_new_content.py
   ```

5. **Update tracking:**
   - Edit `extraction-progress.json` to track what's been processed

### Size Reference
| PDF | Pages | Text Tokens | Chunks |
|-----|-------|-------------|--------|
| Sol System | 113 | ~107k | 12 |
| Ships of The Expanse | 147 | ~101k | 12 |
| TUE Core | 290 | ~284k | 32 |
| Profession PDFs | 15-20 | ~14-17k | 1 |

### Dependencies
```bash
pip install pymupdf  # PyMuPDF for PDF text extraction
```
