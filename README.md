# Gutenberg Website Scraper

A Python script for scraping and processing books from Project Gutenberg (gutenberg.org) for AI and machine learning applications.

## Features

- 📚 Download books from Project Gutenberg by book ID
- 🧹 Automatic text cleaning (removes headers, footers, and metadata)
- 🤖 AI-ready text preprocessing
- 💾 Multiple output formats (JSON, JSONL, TXT)
- ⚡ Caching support to avoid redundant downloads
- 🌐 Rate limiting to be respectful to the server
- 📊 Batch download multiple books

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pewpi-infinity/Gutenberg.git
cd Gutenberg
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Download a single book:
```bash
python gutenberg_scraper.py 1342
```

Download multiple books:
```bash
python gutenberg_scraper.py 1342 11 84 1661 2701
```

Specify output format and file:
```bash
python gutenberg_scraper.py 1342 11 84 -o books.json -f json
```

Save as JSONL (one book per line, good for streaming):
```bash
python gutenberg_scraper.py 1342 11 84 -o books.jsonl -f jsonl
```

Save as plain text:
```bash
python gutenberg_scraper.py 1342 11 84 -o books.txt -f txt
```

Skip text cleaning (keep raw text):
```bash
python gutenberg_scraper.py 1342 --no-clean
```

Customize cache directory and download delay:
```bash
python gutenberg_scraper.py 1342 11 84 --cache-dir ./my_cache --delay 3.0
```

### Python API

```python
from gutenberg_scraper import GutenbergScraper

# Create scraper instance
scraper = GutenbergScraper(cache_dir='my_cache')

# Download a book
book_text = scraper.download_book(1342)  # Pride and Prejudice

# Clean the text
cleaned_text = scraper.clean_gutenberg_text(book_text)

# Preprocess for AI
ai_ready_text = scraper.preprocess_for_ai(cleaned_text)

# Download multiple books
book_ids = [1342, 11, 84, 1661, 2701]  # Classic literature
books = scraper.download_multiple_books(book_ids, delay=2.0)

# Save processed books
scraper.save_processed_books(books, 'output.json', format='json', clean=True)
```

## Popular Book IDs

Here are some popular books available on Project Gutenberg:

- 1342: Pride and Prejudice by Jane Austen
- 11: Alice's Adventures in Wonderland by Lewis Carroll
- 84: Frankenstein by Mary Shelley
- 1661: Sherlock Holmes by Arthur Conan Doyle
- 2701: Moby Dick by Herman Melville
- 46: A Christmas Carol by Charles Dickens
- 98: A Tale of Two Cities by Charles Dickens
- 1513: Romeo and Juliet by William Shakespeare
- 1952: The Yellow Wallpaper by Charlotte Perkins Gilman
- 16328: Beowulf

## Output Formats

### JSON
```json
{
  "1342": "Pride and Prejudice text...",
  "11": "Alice in Wonderland text..."
}
```

### JSONL
```jsonl
{"book_id": 1342, "text": "Pride and Prejudice text..."}
{"book_id": 11, "text": "Alice in Wonderland text..."}
```

### TXT
```
================================================================================
BOOK ID: 1342
================================================================================

Pride and Prejudice text...

================================================================================
BOOK ID: 11
================================================================================

Alice in Wonderland text...
```

## AI/ML Use Cases

This scraper is designed for various AI and machine learning applications:

- **Natural Language Processing (NLP)**: Training language models on classic literature
- **Text Generation**: Fine-tuning GPT models on specific writing styles
- **Sentiment Analysis**: Analyzing emotional patterns in literature
- **Topic Modeling**: Discovering themes across books
- **Text Classification**: Training classifiers on different genres
- **Named Entity Recognition**: Extracting characters and locations
- **Translation**: Building parallel corpora (if using multilingual books)

## Technical Details

### Text Cleaning

The scraper automatically:
- Removes Project Gutenberg headers and footers
- Removes page numbers and metadata
- Normalizes whitespace
- Handles different text encodings (UTF-8, Latin-1)

### Rate Limiting

The scraper includes a configurable delay between downloads (default: 2 seconds) to be respectful to Project Gutenberg's servers. Please be considerate when downloading books.

### Caching

Downloaded books are cached locally to avoid redundant downloads. The cache directory can be customized using the `--cache-dir` option.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is for educational and research purposes. Please respect Project Gutenberg's terms of service and copyright laws.

## Disclaimer

This tool is designed for educational and research purposes. Please use it responsibly and in accordance with Project Gutenberg's Robot Access Guidelines: https://www.gutenberg.org/policy/robot_access.html