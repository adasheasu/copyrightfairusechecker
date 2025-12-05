"""
Document Analyzer Module
Extracts text and metadata from PDF and Word documents
"""

import os
import re
from pathlib import Path
from datetime import datetime


class DocumentAnalyzer:
    """Analyzes documents to extract metadata and copyright information"""

    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'doc', 'txt']

    def analyze(self, document_path):
        """
        Analyze a document file

        Args:
            document_path: Path to the document file

        Returns:
            Dictionary containing analysis results
        """
        results = {
            'author': None,
            'title': None,
            'date': None,
            'metadata': {},
            'text_content': None,
            'copyright_notices': [],
            'citations': [],
            'file_size': None,
            'page_count': None
        }

        try:
            file_path = Path(document_path)
            results['file_size'] = file_path.stat().st_size
            extension = file_path.suffix.lower()

            # Route to appropriate analyzer based on file type
            if extension == '.pdf':
                results.update(self._analyze_pdf(document_path))
            elif extension in ['.docx', '.doc']:
                results.update(self._analyze_word(document_path))
            elif extension == '.txt':
                results.update(self._analyze_text(document_path))

            # Search for copyright notices in text
            if results.get('text_content'):
                results['copyright_notices'] = self._find_copyright_notices(
                    results['text_content']
                )

                # Find citations and attributions
                results['citations'] = self._find_citations(results['text_content'])

        except Exception as e:
            results['error'] = f"Error analyzing document: {str(e)}"

        return results

    def _analyze_pdf(self, pdf_path):
        """Analyze PDF document"""
        results = {}

        try:
            import PyPDF2

            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                # Extract metadata
                metadata = reader.metadata
                if metadata:
                    results['metadata'] = {
                        'author': metadata.get('/Author', None),
                        'title': metadata.get('/Title', None),
                        'subject': metadata.get('/Subject', None),
                        'creator': metadata.get('/Creator', None),
                        'producer': metadata.get('/Producer', None),
                        'creation_date': metadata.get('/CreationDate', None),
                    }

                    if metadata.get('/Author'):
                        results['author'] = metadata.get('/Author')
                    if metadata.get('/Title'):
                        results['title'] = metadata.get('/Title')
                    if metadata.get('/CreationDate'):
                        results['date'] = metadata.get('/CreationDate')

                # Get page count
                results['page_count'] = len(reader.pages)

                # Extract text from first few pages
                text_content = []
                max_pages = min(3, len(reader.pages))  # First 3 pages

                for i in range(max_pages):
                    page = reader.pages[i]
                    text_content.append(page.extract_text())

                results['text_content'] = '\n'.join(text_content)

        except ImportError:
            results['error'] = 'PyPDF2 not installed. Install with: pip install PyPDF2'
        except Exception as e:
            results['error'] = f"Error reading PDF: {str(e)}"

        return results

    def _analyze_word(self, word_path):
        """Analyze Word document"""
        results = {}

        try:
            from docx import Document

            doc = Document(word_path)

            # Extract metadata
            core_properties = doc.core_properties
            results['metadata'] = {
                'author': core_properties.author,
                'title': core_properties.title,
                'subject': core_properties.subject,
                'created': str(core_properties.created) if core_properties.created else None,
                'modified': str(core_properties.modified) if core_properties.modified else None,
                'last_modified_by': core_properties.last_modified_by,
            }

            if core_properties.author:
                results['author'] = core_properties.author
            if core_properties.title:
                results['title'] = core_properties.title
            if core_properties.created:
                results['date'] = str(core_properties.created)

            # Extract text content (first few paragraphs)
            text_content = []
            for i, para in enumerate(doc.paragraphs[:20]):  # First 20 paragraphs
                if para.text.strip():
                    text_content.append(para.text)

            results['text_content'] = '\n'.join(text_content)
            results['page_count'] = 'N/A (Word document)'

        except ImportError:
            results['error'] = 'python-docx not installed. Install with: pip install python-docx'
        except Exception as e:
            results['error'] = f"Error reading Word document: {str(e)}"

        return results

    def _analyze_text(self, text_path):
        """Analyze plain text file"""
        results = {}

        try:
            with open(text_path, 'r', encoding='utf-8') as file:
                content = file.read(5000)  # First 5000 characters
                results['text_content'] = content

        except Exception as e:
            results['error'] = f"Error reading text file: {str(e)}"

        return results

    def _find_copyright_notices(self, text):
        """Find copyright notices in text"""
        notices = []

        # Common copyright patterns
        patterns = [
            r'©\s*\d{4}.*',
            r'Copyright\s*©?\s*\d{4}.*',
            r'\(c\)\s*\d{4}.*',
            r'All rights reserved.*',
            r'No part of this publication may be reproduced.*',
            r'Licensed under.*',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                notice = match.group(0)[:200]  # Limit length
                if notice not in notices:
                    notices.append(notice)

        return notices

    def _find_citations(self, text):
        """Find citations and attributions in text"""
        citations = []

        # Look for common citation patterns
        patterns = [
            r'(?:Image|Photo|Figure)\s+(?:by|from|courtesy of)\s+([^\n.]+)',
            r'Source:\s*([^\n]+)',
            r'Credit:\s*([^\n]+)',
            r'Attribution:\s*([^\n]+)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                citation = match.group(0)[:150]  # Limit length
                if citation not in citations:
                    citations.append(citation)

        return citations


def extract_urls_from_document(text):
    """Helper function to extract URLs from document text"""
    url_pattern = r'https?://[^\s<>"\'\)]+|www\.[^\s<>"\'\\)]+'
    urls = re.findall(url_pattern, text)
    return list(set(urls))  # Remove duplicates


def is_supported_document(filename):
    """Check if file is a supported document format"""
    supported = ['pdf', 'docx', 'doc', 'txt']
    extension = filename.lower().split('.')[-1]
    return extension in supported
