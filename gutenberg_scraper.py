#!/usr/bin/env python3
"""
Gutenberg Website Scraper for AI Applications

This script scrapes books from Project Gutenberg (gutenberg.org) and processes
the text data for AI/ML applications. It provides functionality to:
- Search and download books by ID or search term
- Clean and preprocess text for AI training
- Save processed data in various formats
"""

import requests
import re
import os
import json
import time
from typing import Optional, Dict, List
from urllib.parse import urljoin
import argparse


class GutenbergScraper:
    """
    A scraper for Project Gutenberg that downloads and processes book texts
    for AI and machine learning applications.
    """
    
    BASE_URL = "https://www.gutenberg.org"
    CACHE_DIR = "gutenberg_cache"
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the Gutenberg scraper.
        
        Args:
            cache_dir: Directory to cache downloaded books (default: gutenberg_cache)
        """
        self.cache_dir = cache_dir or self.CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational/Research Purpose)'
        })
    
    def get_book_url(self, book_id: int, format: str = 'txt') -> str:
        """
        Construct the URL for downloading a book.
        
        Args:
            book_id: The Project Gutenberg book ID
            format: File format (txt, html, epub)
        
        Returns:
            URL string for the book
        """
        # Project Gutenberg uses a hierarchical directory structure
        # Example: Book 1234 is at /files/1234/1234-0.txt
        if format == 'txt':
            return f"{self.BASE_URL}/files/{book_id}/{book_id}-0.txt"
        elif format == 'html':
            return f"{self.BASE_URL}/files/{book_id}/{book_id}-h/{book_id}-h.htm"
        else:
            return f"{self.BASE_URL}/ebooks/{book_id}"
    
    def download_book(self, book_id: int, force_refresh: bool = False) -> Optional[str]:
        """
        Download a book from Project Gutenberg.
        
        Args:
            book_id: The Project Gutenberg book ID
            force_refresh: If True, re-download even if cached
        
        Returns:
            The book text as a string, or None if download fails
        """
        cache_file = os.path.join(self.cache_dir, f"book_{book_id}.txt")
        
        # Check cache first
        if not force_refresh and os.path.exists(cache_file):
            print(f"Loading book {book_id} from cache...")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Try downloading the book
        url = self.get_book_url(book_id, 'txt')
        print(f"Downloading book {book_id} from {url}...")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Decode with UTF-8, fallback to latin-1
            try:
                text = response.content.decode('utf-8')
            except UnicodeDecodeError:
                text = response.content.decode('latin-1')
            
            # Cache the downloaded book
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"Successfully downloaded book {book_id}")
            return text
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading book {book_id}: {e}")
            # Try alternative URL format
            alt_url = f"{self.BASE_URL}/files/{book_id}/{book_id}.txt"
            try:
                response = self.session.get(alt_url, timeout=30)
                response.raise_for_status()
                text = response.content.decode('utf-8', errors='ignore')
                
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                print(f"Successfully downloaded book {book_id} from alternate URL")
                return text
            except:
                print(f"Failed to download book {book_id} from alternate URL as well")
                return None
    
    def clean_gutenberg_text(self, text: str) -> str:
        """
        Clean Project Gutenberg text by removing headers, footers, and metadata.
        
        Args:
            text: Raw book text from Project Gutenberg
        
        Returns:
            Cleaned text suitable for AI processing
        """
        # Remove Project Gutenberg header
        start_markers = [
            "*** START OF THIS PROJECT GUTENBERG EBOOK",
            "*** START OF THE PROJECT GUTENBERG EBOOK",
            "*END*THE SMALL PRINT",
        ]
        
        for marker in start_markers:
            if marker in text:
                text = text.split(marker, 1)[1]
                # Remove the rest of the first line after the marker
                text = text.split('\n', 1)[1] if '\n' in text else text
                break
        
        # Remove Project Gutenberg footer
        end_markers = [
            "*** END OF THIS PROJECT GUTENBERG EBOOK",
            "*** END OF THE PROJECT GUTENBERG EBOOK",
            "End of the Project Gutenberg EBook",
            "End of Project Gutenberg's",
        ]
        
        for marker in end_markers:
            if marker in text:
                text = text.split(marker, 1)[0]
                break
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = text.strip()
        
        return text
    
    def preprocess_for_ai(self, text: str, remove_chapter_headers: bool = False) -> str:
        """
        Preprocess text for AI/ML applications.
        
        Args:
            text: Cleaned book text
            remove_chapter_headers: If True, attempt to remove chapter headers
        
        Returns:
            Preprocessed text
        """
        # Remove chapter headers if requested
        if remove_chapter_headers:
            text = re.sub(r'^(CHAPTER|Chapter)\s+[IVXLCDM\d]+.*$', '', text, flags=re.MULTILINE)
        
        # Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove page numbers (common pattern: [Page 123])
        text = re.sub(r'\[Page \d+\]', '', text)
        
        return text.strip()
    
    def get_book_metadata(self, book_id: int) -> Optional[Dict]:
        """
        Fetch metadata for a book from Project Gutenberg.
        
        Args:
            book_id: The Project Gutenberg book ID
        
        Returns:
            Dictionary containing book metadata, or None if unavailable
        """
        # This is a simplified version - full implementation would parse the RDF metadata
        metadata_url = f"{self.BASE_URL}/ebooks/{book_id}"
        
        try:
            response = self.session.get(metadata_url, timeout=30)
            response.raise_for_status()
            
            # Basic metadata extraction from HTML (simplified)
            html = response.text
            
            metadata = {
                'book_id': book_id,
                'url': metadata_url,
                'title': None,
                'author': None,
            }
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            return metadata
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching metadata for book {book_id}: {e}")
            return None
    
    def download_multiple_books(self, book_ids: List[int], delay: float = 2.0) -> Dict[int, str]:
        """
        Download multiple books with rate limiting.
        
        Args:
            book_ids: List of Project Gutenberg book IDs
            delay: Delay in seconds between downloads (to be respectful)
        
        Returns:
            Dictionary mapping book IDs to their text content
        """
        books = {}
        
        for i, book_id in enumerate(book_ids):
            print(f"\nDownloading book {i+1}/{len(book_ids)} (ID: {book_id})")
            text = self.download_book(book_id)
            
            if text:
                books[book_id] = text
            
            # Rate limiting - be respectful to the server
            if i < len(book_ids) - 1:
                time.sleep(delay)
        
        return books
    
    def save_processed_books(self, books: Dict[int, str], output_file: str, 
                           format: str = 'json', clean: bool = True):
        """
        Save processed books to a file.
        
        Args:
            books: Dictionary mapping book IDs to text content
            output_file: Output file path
            format: Output format ('json', 'txt', 'jsonl')
            clean: If True, clean and preprocess the text
        """
        if clean:
            processed_books = {}
            for book_id, text in books.items():
                cleaned = self.clean_gutenberg_text(text)
                preprocessed = self.preprocess_for_ai(cleaned)
                processed_books[book_id] = preprocessed
        else:
            processed_books = books
        
        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_books, f, indent=2, ensure_ascii=False)
            print(f"\nSaved {len(processed_books)} books to {output_file} (JSON format)")
        
        elif format == 'jsonl':
            with open(output_file, 'w', encoding='utf-8') as f:
                for book_id, text in processed_books.items():
                    record = {'book_id': book_id, 'text': text}
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
            print(f"\nSaved {len(processed_books)} books to {output_file} (JSONL format)")
        
        elif format == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                for book_id, text in processed_books.items():
                    f.write(f"\n{'='*80}\n")
                    f.write(f"BOOK ID: {book_id}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(text)
                    f.write("\n\n")
            print(f"\nSaved {len(processed_books)} books to {output_file} (TXT format)")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Scrape books from Project Gutenberg for AI applications'
    )
    parser.add_argument(
        'book_ids',
        type=int,
        nargs='+',
        help='Project Gutenberg book IDs to download'
    )
    parser.add_argument(
        '-o', '--output',
        default='gutenberg_books.json',
        help='Output file path (default: gutenberg_books.json)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'jsonl', 'txt'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--no-clean',
        action='store_true',
        help='Skip text cleaning and preprocessing'
    )
    parser.add_argument(
        '--cache-dir',
        default='gutenberg_cache',
        help='Directory for caching downloaded books'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between downloads in seconds (default: 2.0)'
    )
    
    args = parser.parse_args()
    
    # Create scraper instance
    scraper = GutenbergScraper(cache_dir=args.cache_dir)
    
    # Download books
    print(f"Starting download of {len(args.book_ids)} books...")
    books = scraper.download_multiple_books(args.book_ids, delay=args.delay)
    
    if books:
        # Save processed books
        scraper.save_processed_books(
            books,
            args.output,
            format=args.format,
            clean=not args.no_clean
        )
        print(f"\nSuccessfully processed {len(books)} out of {len(args.book_ids)} books")
    else:
        print("\nNo books were successfully downloaded")


if __name__ == '__main__':
    main()
