"""
Image Analyzer Module
Performs reverse image search and extracts metadata from images
"""

import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
import hashlib
from pathlib import Path


class ImageAnalyzer:
    """Analyzes images to identify sources and extract metadata"""

    def __init__(self):
        self.supported_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']

    def analyze(self, image_path):
        """
        Analyze an image file

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing analysis results
        """
        results = {
            'original_url': None,
            'author': None,
            'title': None,
            'date': None,
            'confidence': None,
            'metadata': {},
            'dimensions': None,
            'file_size': None
        }

        try:
            # Extract basic file info
            file_path = Path(image_path)
            results['file_size'] = file_path.stat().st_size

            # Open and analyze image
            with Image.open(image_path) as img:
                results['dimensions'] = f"{img.width}x{img.height}"
                results['format'] = img.format

                # Extract EXIF metadata
                metadata = self._extract_metadata(img)
                results['metadata'] = metadata

                if metadata:
                    # Try to find author/copyright in metadata
                    if 'Artist' in metadata:
                        results['author'] = metadata['Artist']
                    if 'Copyright' in metadata:
                        results['copyright_notice'] = metadata['Copyright']
                    if 'DateTime' in metadata:
                        results['date'] = metadata['DateTime']

            # Perform reverse image search
            reverse_search_results = self._reverse_image_search(image_path)
            if reverse_search_results:
                results.update(reverse_search_results)

            # Calculate image hash for duplicate detection
            results['image_hash'] = self._calculate_image_hash(image_path)

        except Exception as e:
            results['error'] = f"Error analyzing image: {str(e)}"

        return results

    def _extract_metadata(self, img):
        """Extract EXIF and other metadata from image"""
        metadata = {}

        try:
            # EXIF data
            exifdata = img.getexif()
            if exifdata:
                for tag_id, value in exifdata.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[tag] = str(value)

            # XMP/IPTC metadata (if available)
            if hasattr(img, 'info'):
                for key, value in img.info.items():
                    if key not in metadata:
                        metadata[key] = str(value)

        except Exception as e:
            metadata['extraction_error'] = str(e)

        return metadata

    def _reverse_image_search(self, image_path):
        """
        Perform reverse image search to find original source

        Note: This is a simplified version. In production, you would integrate with:
        - Google Vision API
        - TinEye API
        - Bing Visual Search API
        """
        results = {
            'reverse_search_attempted': True,
            'search_method': 'Simulated (requires API keys for production)'
        }

        # Simulated response - in production this would call actual APIs
        # For demo purposes, we'll check common stock photo patterns
        try:
            with Image.open(image_path) as img:
                # Check for common stock photo watermarks or patterns
                if self._has_watermark(img):
                    results['watermark_detected'] = True
                    results['confidence'] = 'Medium'
                    results['note'] = 'Watermark detected - likely from stock photo service'

                # In production, call reverse image search APIs here
                # Example structure for what the API would return:
                results['api_note'] = (
                    'To enable reverse image search, configure API keys for:\n'
                    '- Google Cloud Vision API\n'
                    '- TinEye API\n'
                    '- Bing Visual Search API'
                )

        except Exception as e:
            results['error'] = str(e)

        return results

    def _has_watermark(self, img):
        """Simple watermark detection (simplified version)"""
        # This is a placeholder - real watermark detection would use
        # computer vision techniques
        return False

    def _calculate_image_hash(self, image_path):
        """Calculate perceptual hash of image for duplicate detection"""
        try:
            with Image.open(image_path) as img:
                # Convert to grayscale and resize for consistent hashing
                img = img.convert('L').resize((8, 8), Image.Resampling.LANCZOS)

                # Get pixel data
                pixels = list(img.getdata())

                # Calculate average
                avg = sum(pixels) / len(pixels)

                # Create hash based on whether pixels are above/below average
                bits = ''.join('1' if pixel > avg else '0' for pixel in pixels)

                # Convert to hex
                return hex(int(bits, 2))

        except Exception as e:
            return f"Error: {str(e)}"

    def search_commons_wikimedia(self, query):
        """
        Search Wikimedia Commons for similar free images

        Args:
            query: Search query string

        Returns:
            List of alternative images from Wikimedia Commons
        """
        results = []

        try:
            # Wikimedia Commons API search
            url = "https://commons.wikimedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'generator': 'search',
                'gsrsearch': query,
                'gsrlimit': 5,
                'prop': 'imageinfo',
                'iiprop': 'url|extmetadata'
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'pages' in data['query']:
                    for page in data['query']['pages'].values():
                        if 'imageinfo' in page:
                            results.append({
                                'title': page.get('title', 'Unknown'),
                                'url': page['imageinfo'][0].get('url'),
                                'license': 'Wikimedia Commons (Various licenses)',
                                'source': 'Wikimedia Commons'
                            })

        except Exception as e:
            pass  # Fail silently, return empty results

        return results


def get_image_dimensions(image_path):
    """Helper function to get image dimensions"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return None


def is_supported_image(filename):
    """Check if file is a supported image format"""
    supported = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
    extension = filename.lower().split('.')[-1]
    return extension in supported
