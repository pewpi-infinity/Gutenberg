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
BOOK ID: 1342

Pride and Prejudice text...

BOOK ID: 11

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
# Gutenberg

## Progress Monitor System

A robust progress monitoring system designed to help you **keep an eye on the prize** and ensure that automated processes (like ChatGPT or other AI systems) **don't fail partway through** tasks.

### Features

✅ **Goal-Oriented Tracking** - Define clear goals and track progress towards them  
✅ **Task Management** - Break down goals into manageable tasks  
✅ **Progress Monitoring** - Real-time progress updates with percentage tracking  
✅ **Checkpoint System** - Create recovery points to prevent data loss  
✅ **Failure Recovery** - Automatically recover from the last checkpoint when failures occur  
✅ **State Persistence** - All progress is saved to disk and survives restarts  
✅ **CLI Interface** - Easy-to-use command-line tool  
✅ **Programmatic API** - Python library for integration into your projects  

### Installation

No installation required! Just use the Python files directly:

```bash
# Clone or download the repository
git clone https://github.com/pewpi-infinity/Gutenberg.git
cd Gutenberg

# Make the CLI executable (optional)
chmod +x progress_cli.py
```

### Quick Start

#### Using the CLI

```bash
# 1. Create a new progress monitor with a goal
python3 progress_cli.py create --goal "Complete the project without failing"

# 2. Add tasks
python3 progress_cli.py add-task --task-id task1 --name "Design" --description "Create designs"
python3 progress_cli.py add-task --task-id task2 --name "Implement" --description "Write code"
python3 progress_cli.py add-task --task-id task3 --name "Test" --description "Run tests"

# 3. Start working on tasks
python3 progress_cli.py start --task-id task1

# 4. Update progress with checkpoints
python3 progress_cli.py update --task-id task1 --percentage 50 --checkpoint "Mockups complete"
python3 progress_cli.py update --task-id task1 --percentage 100

# 5. Complete the task
python3 progress_cli.py complete --task-id task1

# 6. Check status anytime
python3 progress_cli.py status
```

#### Handling Failures

The system is designed to handle failures gracefully:

```bash
# If a task fails
python3 progress_cli.py fail --task-id task2 --reason "Connection timeout"

# Recover from the last checkpoint
python3 progress_cli.py recover --task-id task2

# Continue from where you left off
python3 progress_cli.py update --task-id task2 --percentage 100
python3 progress_cli.py complete --task-id task2
```

#### Using the Python API

```python
from progress_monitor import ProgressMonitor

# Create a monitor
monitor = ProgressMonitor("Complete the Gutenberg project")

# Add tasks
monitor.add_task("design", "Design System", "Create the design system")
monitor.add_task("implement", "Implementation", "Implement core features")

# Work on tasks
monitor.start_task("design")
monitor.update_progress("design", 50, "Initial mockups done")
monitor.update_progress("design", 100, "Final designs approved")
monitor.complete_task("design")

# Handle failures
monitor.start_task("implement")
monitor.update_progress("implement", 60, "API integration complete")
monitor.fail_task("implement", "Connection lost")

# Recover and continue
checkpoint = monitor.recover_task("implement")
print(f"Recovered from: {checkpoint['name']} at {checkpoint['progress']}%")

monitor.update_progress("implement", 100)
monitor.complete_task("implement")

# Check if goal is achieved
if monitor.is_goal_achieved():
    print("🎉 Goal achieved!")

# Print status
monitor.print_status()
```

### Example Output

```
Goal: Don't let ChatGPT fail partway through
Overall Progress: 100.0%
Goal Achieved: True

Tasks:
  ✅ [100.0%] Analysis
      Status: completed
      Checkpoints: 1
  ✅ [100.0%] Implementation
      Status: completed
      Checkpoints: 2
  ✅ [100.0%] Verification
      Status: completed

🎉 CONGRATULATIONS! Goal achieved! All tasks completed! 🎉
```

### Architecture

The system consists of three main components:

1. **`progress_monitor.py`** - Core library with `ProgressMonitor` and `Task` classes
2. **`progress_cli.py`** - Command-line interface for easy interaction
3. **`test_progress_monitor.py`** - Comprehensive test suite

### State Persistence

All progress is automatically saved to a JSON file (default: `progress_state.json`). This means:
- Progress survives system crashes and restarts
- You can share progress with team members
- You can backup and restore your progress
- Multiple monitors can use different state files

### Use Cases

- **AI Task Monitoring** - Ensure ChatGPT/AI agents complete tasks fully
- **Long-Running Processes** - Track progress of builds, deployments, data processing
- **Project Management** - Break down projects into trackable tasks
- **Automated Workflows** - Add checkpoints to prevent partial failures
- **Team Collaboration** - Share progress state across team members

### Testing

Run the comprehensive test suite:

```bash
python3 -m unittest test_progress_monitor.py -v
```

All 22 tests should pass, covering:
- Task creation and management
- Progress tracking and updates
- Checkpoint creation and recovery
- State persistence and loading
- Error handling
- Goal achievement detection

### Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

### License

Open source - feel free to use and modify as needed.

### Contributing

Contributions welcome! This system is designed to be simple and focused on preventing partial failures through checkpoints and state persistence.
