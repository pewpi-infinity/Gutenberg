#!/usr/bin/env python3
"""
Unit tests for Gutenberg scraper functionality.

Tests the text processing and cleaning functions without requiring internet access.
"""

import unittest
import os
import json
import tempfile
from gutenberg_scraper import GutenbergScraper


class TestGutenbergScraper(unittest.TestCase):
    """Test cases for GutenbergScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = GutenbergScraper(cache_dir=tempfile.mkdtemp())
        
        # Sample Project Gutenberg text with header and footer
        self.sample_text = """The Project Gutenberg EBook of Test Book

This eBook is for the use of anyone anywhere.

*** START OF THIS PROJECT GUTENBERG EBOOK TEST BOOK ***

CHAPTER I

This is the actual content of the book.
It has multiple lines and paragraphs.

This is another paragraph with some text.


CHAPTER II

More content here.

*** END OF THIS PROJECT GUTENBERG EBOOK TEST BOOK ***

End of the Project Gutenberg EBook of Test Book
"""
    
    def test_clean_gutenberg_text(self):
        """Test that Gutenberg headers and footers are removed."""
        cleaned = self.scraper.clean_gutenberg_text(self.sample_text)
        
        # Check that header is removed
        self.assertNotIn("*** START OF THIS PROJECT GUTENBERG", cleaned)
        
        # Check that footer is removed
        self.assertNotIn("*** END OF THIS PROJECT GUTENBERG", cleaned)
        
        # Check that actual content is preserved
        self.assertIn("This is the actual content", cleaned)
        self.assertIn("More content here", cleaned)
    
    def test_preprocess_for_ai(self):
        """Test AI preprocessing functions."""
        text = "This is a test.    Multiple   spaces.\n\n\n\nMultiple newlines."
        processed = self.scraper.preprocess_for_ai(text)
        
        # Check that multiple spaces are normalized
        self.assertNotIn("    ", processed)
        self.assertNotIn("   ", processed)
        
        # Check that text is preserved
        self.assertIn("This is a test", processed)
    
    def test_preprocess_remove_chapter_headers(self):
        """Test chapter header removal."""
        text = """CHAPTER I

Content here.

CHAPTER II

More content.

Chapter III

Even more content."""
        
        processed = self.scraper.preprocess_for_ai(text, remove_chapter_headers=True)
        
        # Check that chapter headers are removed
        self.assertNotIn("CHAPTER I", processed)
        self.assertNotIn("CHAPTER II", processed)
        self.assertNotIn("Chapter III", processed)
        
        # Check that content is preserved
        self.assertIn("Content here", processed)
        self.assertIn("More content", processed)
    
    def test_get_book_url(self):
        """Test URL construction for different book IDs."""
        url = self.scraper.get_book_url(1342, 'txt')
        self.assertEqual(url, "https://www.gutenberg.org/files/1342/1342-0.txt")
        
        url = self.scraper.get_book_url(11, 'txt')
        self.assertEqual(url, "https://www.gutenberg.org/files/11/11-0.txt")
    
    def test_save_processed_books_json(self):
        """Test saving books in JSON format."""
        books = {
            1: "Book one content",
            2: "Book two content"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_file = f.name
        
        try:
            self.scraper.save_processed_books(books, output_file, format='json', clean=False)
            
            # Read back and verify
            with open(output_file, 'r') as f:
                loaded = json.load(f)
            
            self.assertEqual(len(loaded), 2)
            self.assertIn('1', loaded)
            self.assertIn('2', loaded)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def test_save_processed_books_jsonl(self):
        """Test saving books in JSONL format."""
        books = {
            1: "Book one content",
            2: "Book two content"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            output_file = f.name
        
        try:
            self.scraper.save_processed_books(books, output_file, format='jsonl', clean=False)
            
            # Read back and verify
            with open(output_file, 'r') as f:
                lines = f.readlines()
            
            self.assertEqual(len(lines), 2)
            
            record1 = json.loads(lines[0])
            self.assertIn('book_id', record1)
            self.assertIn('text', record1)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def test_save_processed_books_txt(self):
        """Test saving books in TXT format."""
        books = {
            1: "Book one content",
            2: "Book two content"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            output_file = f.name
        
        try:
            self.scraper.save_processed_books(books, output_file, format='txt', clean=False)
            
            # Read back and verify
            with open(output_file, 'r') as f:
                content = f.read()
            
            self.assertIn("BOOK ID: 1", content)
            self.assertIn("BOOK ID: 2", content)
            self.assertIn("Book one content", content)
            self.assertIn("Book two content", content)
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def test_clean_with_preprocessing(self):
        """Test full cleaning and preprocessing pipeline."""
        cleaned = self.scraper.clean_gutenberg_text(self.sample_text)
        processed = self.scraper.preprocess_for_ai(cleaned)
        
        # Should have actual content
        self.assertGreater(len(processed), 0)
        
        # Should not have headers/footers
        self.assertNotIn("START OF THIS PROJECT", processed)
        self.assertNotIn("END OF THIS PROJECT", processed)


class TestTextProcessing(unittest.TestCase):
    """Test text processing edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = GutenbergScraper()
    
    def test_empty_text(self):
        """Test handling of empty text."""
        cleaned = self.scraper.clean_gutenberg_text("")
        self.assertEqual(cleaned, "")
        
        processed = self.scraper.preprocess_for_ai("")
        self.assertEqual(processed, "")
    
    def test_text_without_markers(self):
        """Test text without Gutenberg markers."""
        text = "This is just regular text without any markers."
        cleaned = self.scraper.clean_gutenberg_text(text)
        
        # Should return text unchanged (minus whitespace normalization)
        self.assertIn("regular text", cleaned)
    
    def test_whitespace_normalization(self):
        """Test that excessive whitespace is normalized."""
        text = "Line 1\n\n\n\n\nLine 2"
        cleaned = self.scraper.clean_gutenberg_text(text)
        
        # Should have at most double newlines
        self.assertNotIn("\n\n\n", cleaned)


def run_tests():
    """Run all tests."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
