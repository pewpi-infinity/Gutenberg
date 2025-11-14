#!/usr/bin/env python3
"""
Example usage of the Gutenberg scraper for AI applications.

This script demonstrates how to use the scraper to download and process
books for machine learning and natural language processing tasks.
"""

from gutenberg_scraper import GutenbergScraper
import json


def example_basic_usage():
    """Basic example: Download and clean a single book."""
    print("=== Example 1: Basic Usage ===\n")
    
    scraper = GutenbergScraper()
    
    # Download Pride and Prejudice
    book_id = 1342
    print(f"Downloading book {book_id}...")
    text = scraper.download_book(book_id)
    
    if text:
        print(f"Downloaded {len(text)} characters")
        
        # Clean the text
        cleaned = scraper.clean_gutenberg_text(text)
        print(f"After cleaning: {len(cleaned)} characters")
        
        # Show first 500 characters
        print(f"\nFirst 500 characters of cleaned text:")
        print(cleaned[:500])
        print("...\n")


def example_batch_download():
    """Example: Download multiple classic books."""
    print("=== Example 2: Batch Download ===\n")
    
    scraper = GutenbergScraper()
    
    # Famous classic literature
    book_ids = [
        1342,  # Pride and Prejudice
        11,    # Alice's Adventures in Wonderland
        84,    # Frankenstein
        1661,  # Sherlock Holmes
        2701,  # Moby Dick
    ]
    
    print(f"Downloading {len(book_ids)} books...")
    books = scraper.download_multiple_books(book_ids, delay=1.0)
    
    print(f"\nSuccessfully downloaded {len(books)} books")
    
    # Save as JSON
    scraper.save_processed_books(books, 'classic_literature.json', format='json')
    
    # Calculate total words
    total_words = 0
    for book_id, text in books.items():
        cleaned = scraper.clean_gutenberg_text(text)
        word_count = len(cleaned.split())
        total_words += word_count
        print(f"Book {book_id}: {word_count:,} words")
    
    print(f"\nTotal corpus: {total_words:,} words")


def example_ai_preprocessing():
    """Example: Preprocess text for AI/ML applications."""
    print("=== Example 3: AI Preprocessing ===\n")
    
    scraper = GutenbergScraper()
    
    # Download a book
    book_id = 11  # Alice's Adventures in Wonderland
    text = scraper.download_book(book_id)
    
    if text:
        # Clean and preprocess
        cleaned = scraper.clean_gutenberg_text(text)
        preprocessed = scraper.preprocess_for_ai(cleaned, remove_chapter_headers=True)
        
        print(f"Original length: {len(text)} characters")
        print(f"Cleaned length: {len(cleaned)} characters")
        print(f"Preprocessed length: {len(preprocessed)} characters")
        
        # Split into sentences (simple approach)
        sentences = [s.strip() for s in preprocessed.split('.') if s.strip()]
        print(f"\nExtracted {len(sentences)} sentences")
        print("\nSample sentences:")
        for i, sentence in enumerate(sentences[:5], 1):
            print(f"{i}. {sentence}")


def example_jsonl_format():
    """Example: Save in JSONL format for streaming."""
    print("=== Example 4: JSONL Format ===\n")
    
    scraper = GutenbergScraper()
    
    # Download a few short books
    book_ids = [1342, 11, 46]  # Pride and Prejudice, Alice, Christmas Carol
    
    books = scraper.download_multiple_books(book_ids, delay=1.0)
    
    # Save as JSONL (one book per line)
    scraper.save_processed_books(books, 'books.jsonl', format='jsonl')
    
    # Read back and process line by line
    print("\nReading JSONL file line by line:")
    with open('books.jsonl', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            record = json.loads(line)
            book_id = record['book_id']
            text_length = len(record['text'])
            print(f"Line {i}: Book {book_id} - {text_length:,} characters")


def example_custom_cache():
    """Example: Use custom cache directory."""
    print("=== Example 5: Custom Cache ===\n")
    
    # Use a custom cache directory
    scraper = GutenbergScraper(cache_dir='my_book_cache')
    
    book_id = 1342
    
    # First download - will fetch from internet
    print("First download (from internet):")
    text1 = scraper.download_book(book_id)
    
    # Second download - will use cache
    print("\nSecond download (from cache):")
    text2 = scraper.download_book(book_id)
    
    # Force refresh
    print("\nForced refresh (from internet):")
    text3 = scraper.download_book(book_id, force_refresh=True)
    
    print(f"\nAll downloads returned same content: {text1 == text2 == text3}")


def main():
    """Run all examples."""
    print("Gutenberg Scraper Examples")
    print("=" * 80)
    print()
    
    examples = [
        example_basic_usage,
        example_batch_download,
        example_ai_preprocessing,
        example_jsonl_format,
        example_custom_cache,
    ]
    
    for example in examples:
        try:
            example()
            print()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            print()
    
    print("=" * 80)
    print("Examples completed!")


if __name__ == '__main__':
    main()
