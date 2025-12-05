"""
Copyright Checker Module
Identifies copyright status and licensing information
"""

import re
import requests
from pathlib import Path


class CopyrightChecker:
    """Checks copyright and licensing information for content"""

    def __init__(self):
        self.creative_commons_licenses = {
            'CC0': 'Public Domain Dedication',
            'CC BY': 'Attribution',
            'CC BY-SA': 'Attribution-ShareAlike',
            'CC BY-ND': 'Attribution-NoDerivs',
            'CC BY-NC': 'Attribution-NonCommercial',
            'CC BY-NC-SA': 'Attribution-NonCommercial-ShareAlike',
            'CC BY-NC-ND': 'Attribution-NonCommercial-NoDerivs',
        }

    def check_image(self, image_path):
        """
        Check copyright status of an image

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with copyright information
        """
        results = {
            'license_type': None,
            'copyright_holder': None,
            'year': None,
            'restrictions': [],
            'attribution_required': False,
            'attribution_text': None,
            'commercial_use_allowed': None,
            'modifications_allowed': None,
            'is_public_domain': False,
            'confidence': 'Low'
        }

        try:
            # Check image metadata for copyright info
            from PIL import Image
            from PIL.ExifTags import TAGS

            with Image.open(image_path) as img:
                exifdata = img.getexif()

                if exifdata:
                    for tag_id, value in exifdata.items():
                        tag = TAGS.get(tag_id, tag_id)

                        if tag == 'Copyright':
                            results['copyright_holder'] = value
                            results['confidence'] = 'Medium'

                            # Parse copyright year
                            year_match = re.search(r'\b(19|20)\d{2}\b', value)
                            if year_match:
                                results['year'] = year_match.group(0)

                        elif tag == 'Artist':
                            if not results['copyright_holder']:
                                results['copyright_holder'] = value

                # Check for Creative Commons license in metadata
                if hasattr(img, 'info'):
                    for key, value in img.info.items():
                        if 'license' in key.lower() or 'rights' in key.lower():
                            cc_license = self._detect_cc_license(str(value))
                            if cc_license:
                                results.update(cc_license)

            # If no metadata found, make conservative assumptions
            if not results['license_type']:
                results['license_type'] = 'Unknown - Assume All Rights Reserved'
                results['restrictions'] = [
                    'Copyright status unknown',
                    'Assume full copyright protection',
                    'Seek permission before use'
                ]
                results['commercial_use_allowed'] = False
                results['modifications_allowed'] = False

        except Exception as e:
            results['error'] = f"Error checking image copyright: {str(e)}"

        return results

    def check_document(self, document_path):
        """
        Check copyright status of a document

        Args:
            document_path: Path to document file

        Returns:
            Dictionary with copyright information
        """
        results = {
            'license_type': None,
            'copyright_holder': None,
            'year': None,
            'restrictions': [],
            'attribution_required': False,
            'attribution_text': None,
            'commercial_use_allowed': None,
            'modifications_allowed': None,
            'is_public_domain': False,
            'confidence': 'Low',
            'copyright_notices': []
        }

        try:
            extension = Path(document_path).suffix.lower()

            # Get document metadata and text
            metadata = {}
            text_content = ''

            if extension == '.pdf':
                doc_info = self._extract_pdf_info(document_path)
                metadata = doc_info.get('metadata', {})
                text_content = doc_info.get('text', '')

            elif extension in ['.docx', '.doc']:
                doc_info = self._extract_word_info(document_path)
                metadata = doc_info.get('metadata', {})
                text_content = doc_info.get('text', '')

            # Check metadata for copyright
            if metadata.get('author'):
                results['copyright_holder'] = metadata['author']

            # Search text for copyright notices
            copyright_info = self._parse_copyright_text(text_content)
            results.update(copyright_info)

            # Detect Creative Commons license
            cc_license = self._detect_cc_license(text_content)
            if cc_license:
                results.update(cc_license)

            # Check for public domain indicators
            if self._is_public_domain(text_content, metadata):
                results['is_public_domain'] = True
                results['license_type'] = 'Public Domain'
                results['commercial_use_allowed'] = True
                results['modifications_allowed'] = True
                results['restrictions'] = []
                results['confidence'] = 'High'

            # If no clear license found
            if not results['license_type'] and not results['is_public_domain']:
                results['license_type'] = 'Unknown - Assume All Rights Reserved'
                results['restrictions'] = [
                    'No clear license identified',
                    'Assume full copyright protection',
                    'May require permission for educational use'
                ]
                results['commercial_use_allowed'] = False
                results['modifications_allowed'] = False

        except Exception as e:
            results['error'] = f"Error checking document copyright: {str(e)}"

        return results

    def _extract_pdf_info(self, pdf_path):
        """Extract info from PDF"""
        info = {'metadata': {}, 'text': ''}

        try:
            import PyPDF2

            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                # Metadata
                if reader.metadata:
                    info['metadata'] = {
                        'author': reader.metadata.get('/Author', None),
                        'title': reader.metadata.get('/Title', None),
                        'subject': reader.metadata.get('/Subject', None),
                    }

                # Text from first few pages
                text_parts = []
                for i in range(min(5, len(reader.pages))):
                    text_parts.append(reader.pages[i].extract_text())
                info['text'] = '\n'.join(text_parts)

        except Exception:
            pass

        return info

    def _extract_word_info(self, word_path):
        """Extract info from Word document"""
        info = {'metadata': {}, 'text': ''}

        try:
            from docx import Document

            doc = Document(word_path)

            # Metadata
            props = doc.core_properties
            info['metadata'] = {
                'author': props.author,
                'title': props.title,
            }

            # Text from first paragraphs
            text_parts = []
            for para in doc.paragraphs[:30]:
                if para.text.strip():
                    text_parts.append(para.text)
            info['text'] = '\n'.join(text_parts)

        except Exception:
            pass

        return info

    def _parse_copyright_text(self, text):
        """Parse copyright information from text"""
        results = {
            'copyright_notices': []
        }

        # Copyright symbol patterns
        copyright_patterns = [
            r'©\s*(\d{4})\s*([^.\n]+)',
            r'Copyright\s*©?\s*(\d{4})\s*([^.\n]+)',
            r'\(c\)\s*(\d{4})\s*([^.\n]+)',
        ]

        for pattern in copyright_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                year = match.group(1)
                holder = match.group(2).strip()[:100]

                if not results.get('year'):
                    results['year'] = year
                if not results.get('copyright_holder'):
                    results['copyright_holder'] = holder

                notice = f"© {year} {holder}"
                if notice not in results['copyright_notices']:
                    results['copyright_notices'].append(notice)

        # Check for "All Rights Reserved"
        if re.search(r'all rights reserved', text, re.IGNORECASE):
            results['license_type'] = 'All Rights Reserved'
            results['commercial_use_allowed'] = False
            results['modifications_allowed'] = False
            results['restrictions'] = ['All rights reserved by copyright holder']
            results['confidence'] = 'High'

        return results

    def _detect_cc_license(self, text):
        """Detect Creative Commons license"""
        results = {}

        text_lower = text.lower()

        # Check for specific CC licenses
        for license_code, license_name in self.creative_commons_licenses.items():
            if license_code.lower() in text_lower:
                results['license_type'] = f'Creative Commons {license_name}'
                results['attribution_required'] = 'BY' in license_code
                results['commercial_use_allowed'] = 'NC' not in license_code
                results['modifications_allowed'] = 'ND' not in license_code
                results['is_public_domain'] = license_code == 'CC0'
                results['confidence'] = 'High'

                # Build restrictions list
                restrictions = []
                if 'BY' in license_code:
                    restrictions.append('Attribution required')
                if 'NC' in license_code:
                    restrictions.append('Non-commercial use only')
                if 'ND' in license_code:
                    restrictions.append('No derivatives allowed')
                if 'SA' in license_code:
                    restrictions.append('Share-alike required')

                results['restrictions'] = restrictions

                # Generate attribution text if author is known
                if results.get('copyright_holder'):
                    results['attribution_text'] = (
                        f'"{results.get("title", "Work")}" by {results["copyright_holder"]} '
                        f'is licensed under {license_code}'
                    )

                break

        return results

    def _is_public_domain(self, text, metadata):
        """Check if content is in public domain"""

        # Check for explicit public domain statements
        pd_indicators = [
            'public domain',
            'no rights reserved',
            'cc0',
            'creative commons zero',
        ]

        text_lower = text.lower()
        for indicator in pd_indicators:
            if indicator in text_lower:
                return True

        # Check publication date (works before 1928 in US)
        year_match = re.search(r'\b(18|19)\d{2}\b', text)
        if year_match:
            year = int(year_match.group(0))
            if year < 1928:
                return True

        return False

    def check_url_license(self, url):
        """
        Check license information from a URL

        Args:
            url: URL to check

        Returns:
            Dictionary with license information
        """
        results = {
            'url': url,
            'license_type': None,
            'source': None
        }

        try:
            # Check if URL is from known open content sources
            if 'commons.wikimedia.org' in url:
                results['source'] = 'Wikimedia Commons'
                results['license_type'] = 'Various - Check specific file'
                results['commercial_use_allowed'] = True  # Most are free
                results['attribution_required'] = True

            elif 'unsplash.com' in url:
                results['source'] = 'Unsplash'
                results['license_type'] = 'Unsplash License'
                results['commercial_use_allowed'] = True
                results['attribution_required'] = False

            elif 'pexels.com' in url:
                results['source'] = 'Pexels'
                results['license_type'] = 'Pexels License'
                results['commercial_use_allowed'] = True
                results['attribution_required'] = False

            elif 'pixabay.com' in url:
                results['source'] = 'Pixabay'
                results['license_type'] = 'Pixabay License'
                results['commercial_use_allowed'] = True
                results['attribution_required'] = False

            elif 'flickr.com' in url:
                results['source'] = 'Flickr'
                results['license_type'] = 'Various - Check specific photo'
                results['note'] = 'Flickr hosts both copyrighted and CC-licensed content'

        except Exception as e:
            results['error'] = str(e)

        return results


def is_creative_commons(license_type):
    """Check if license is a Creative Commons license"""
    if not license_type:
        return False
    return 'creative commons' in license_type.lower() or license_type.startswith('CC')


def is_open_license(license_type):
    """Check if license allows free use"""
    if not license_type:
        return False

    open_indicators = [
        'public domain',
        'cc0',
        'cc by',
        'creative commons',
        'mit',
        'apache',
        'gpl'
    ]

    return any(indicator in license_type.lower() for indicator in open_indicators)
