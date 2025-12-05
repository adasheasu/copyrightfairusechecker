"""
Alternative Finder Module
Suggests alternative content sources when original content cannot be used
"""

import requests


class AlternativeFinder:
    """Finds alternative openly-licensed content"""

    def __init__(self):
        self.open_sources = {
            'images': [
                {
                    'name': 'Wikimedia Commons',
                    'url': 'https://commons.wikimedia.org',
                    'license': 'Various Creative Commons and Public Domain',
                    'api': True
                },
                {
                    'name': 'Unsplash',
                    'url': 'https://unsplash.com',
                    'license': 'Unsplash License (Free for commercial and non-commercial use)',
                    'api': True
                },
                {
                    'name': 'Pexels',
                    'url': 'https://pexels.com',
                    'license': 'Pexels License (Free)',
                    'api': True
                },
                {
                    'name': 'Pixabay',
                    'url': 'https://pixabay.com',
                    'license': 'Pixabay License (Free)',
                    'api': True
                },
                {
                    'name': 'NASA Image Gallery',
                    'url': 'https://images.nasa.gov',
                    'license': 'Public Domain (most images)',
                    'api': True
                },
                {
                    'name': 'Library of Congress',
                    'url': 'https://www.loc.gov/pictures/',
                    'license': 'Many public domain images',
                    'api': True
                }
            ],
            'documents': [
                {
                    'name': 'Project Gutenberg',
                    'url': 'https://www.gutenberg.org',
                    'license': 'Public Domain',
                    'description': '70,000+ free ebooks'
                },
                {
                    'name': 'Open Textbook Library',
                    'url': 'https://open.umn.edu/opentextbooks',
                    'license': 'Creative Commons',
                    'description': 'Free, peer-reviewed textbooks'
                },
                {
                    'name': 'OpenStax',
                    'url': 'https://openstax.org',
                    'license': 'Creative Commons BY',
                    'description': 'Free textbooks for college courses'
                },
                {
                    'name': 'MIT OpenCourseWare',
                    'url': 'https://ocw.mit.edu',
                    'license': 'Creative Commons BY-NC-SA',
                    'description': 'Course materials from MIT'
                },
                {
                    'name': 'OER Commons',
                    'url': 'https://www.oercommons.org',
                    'license': 'Various open licenses',
                    'description': 'Open Educational Resources'
                },
                {
                    'name': 'Internet Archive',
                    'url': 'https://archive.org',
                    'license': 'Various, including Public Domain',
                    'description': 'Digital library of books, media, and more'
                }
            ]
        }

    def find_alternatives(self, source_info, copyright_info):
        """
        Find alternative content sources

        Args:
            source_info: Information about the original content
            copyright_info: Copyright/license information

        Returns:
            List of alternative sources
        """
        alternatives = []

        # Determine content type
        content_type = self._determine_content_type(source_info)

        # Get general alternatives based on content type
        if content_type == 'image':
            alternatives.extend(self._get_image_alternatives(source_info))
        elif content_type == 'document':
            alternatives.extend(self._get_document_alternatives(source_info))

        # Try to find specific alternatives based on content
        specific_alternatives = self._search_specific_alternatives(
            source_info,
            content_type
        )
        alternatives.extend(specific_alternatives)

        # Add educational-specific sources
        educational_sources = self._get_educational_sources(content_type)
        alternatives.extend(educational_sources)

        return alternatives

    def _determine_content_type(self, source_info):
        """Determine if content is image or document"""
        if not source_info:
            return 'unknown'

        file_type = source_info.get('file_type', '').lower()

        if file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
            return 'image'
        elif file_type in ['pdf', 'docx', 'doc', 'txt']:
            return 'document'

        return 'unknown'

    def _get_image_alternatives(self, source_info):
        """Get alternative image sources"""
        alternatives = []

        for source in self.open_sources['images']:
            alternatives.append({
                'source': source['name'],
                'url': source['url'],
                'license': source['license'],
                'description': f'Search {source["name"]} for similar images',
                'type': 'general_resource'
            })

        return alternatives

    def _get_document_alternatives(self, source_info):
        """Get alternative document sources"""
        alternatives = []

        for source in self.open_sources['documents']:
            alternatives.append({
                'source': source['name'],
                'url': source['url'],
                'license': source['license'],
                'description': source.get('description', ''),
                'type': 'general_resource'
            })

        return alternatives

    def _search_specific_alternatives(self, source_info, content_type):
        """Search for specific alternative content"""
        alternatives = []

        # Extract search terms from source info
        search_terms = self._extract_search_terms(source_info)

        if not search_terms:
            return alternatives

        # Search Wikimedia Commons
        if content_type == 'image':
            wikimedia_results = self._search_wikimedia(search_terms)
            alternatives.extend(wikimedia_results)

        return alternatives

    def _extract_search_terms(self, source_info):
        """Extract relevant search terms from source info"""
        terms = []

        if source_info.get('title'):
            terms.append(source_info['title'])

        if source_info.get('author'):
            terms.append(source_info['author'])

        # For metadata
        metadata = source_info.get('metadata', {})
        if isinstance(metadata, dict):
            if metadata.get('subject'):
                terms.append(metadata['subject'])

        return ' '.join(terms)[:100]  # Limit length

    def _search_wikimedia(self, query):
        """Search Wikimedia Commons for alternatives"""
        alternatives = []

        try:
            url = "https://commons.wikimedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'generator': 'search',
                'gsrsearch': query,
                'gsrlimit': 3,
                'prop': 'imageinfo',
                'iiprop': 'url|extmetadata'
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()

                if 'query' in data and 'pages' in data['query']:
                    for page in data['query']['pages'].values():
                        if 'imageinfo' in page and len(page['imageinfo']) > 0:
                            info = page['imageinfo'][0]

                            # Try to get license info from metadata
                            license_text = 'Wikimedia Commons (Check specific license)'
                            if 'extmetadata' in info:
                                if 'LicenseShortName' in info['extmetadata']:
                                    license_text = info['extmetadata']['LicenseShortName'].get('value', license_text)

                            alternatives.append({
                                'source': 'Wikimedia Commons',
                                'title': page.get('title', 'Unknown').replace('File:', ''),
                                'url': info.get('descriptionurl', ''),
                                'image_url': info.get('url', ''),
                                'license': license_text,
                                'description': 'Similar image from Wikimedia Commons',
                                'type': 'specific_match'
                            })

        except Exception as e:
            # Fail silently
            pass

        return alternatives

    def _get_educational_sources(self, content_type):
        """Get sources specifically for educational use"""
        educational = []

        if content_type == 'image':
            educational.extend([
                {
                    'source': 'Smithsonian Open Access',
                    'url': 'https://www.si.edu/openaccess',
                    'license': 'CC0 (Public Domain)',
                    'description': '3+ million images from Smithsonian museums',
                    'type': 'educational_specific'
                },
                {
                    'source': 'Metropolitan Museum of Art',
                    'url': 'https://www.metmuseum.org/art/collection',
                    'license': 'CC0 (Public Domain) for many works',
                    'description': '400,000+ artworks with open access',
                    'type': 'educational_specific'
                },
                {
                    'source': 'Europeana',
                    'url': 'https://www.europeana.eu',
                    'license': 'Various open licenses',
                    'description': 'European cultural heritage collections',
                    'type': 'educational_specific'
                }
            ])

        elif content_type == 'document':
            educational.extend([
                {
                    'source': 'MERLOT',
                    'url': 'https://www.merlot.org',
                    'license': 'Various open licenses',
                    'description': 'Curated collection of free educational materials',
                    'type': 'educational_specific'
                },
                {
                    'source': 'Khan Academy',
                    'url': 'https://www.khanacademy.org',
                    'license': 'Creative Commons BY-NC-SA',
                    'description': 'Free educational content and exercises',
                    'type': 'educational_specific'
                },
                {
                    'source': 'OpenLearn',
                    'url': 'https://www.open.edu/openlearn/',
                    'license': 'Creative Commons BY-NC-SA',
                    'description': 'Free courses from The Open University',
                    'type': 'educational_specific'
                }
            ])

        return educational

    def search_by_topic(self, topic, content_type='image'):
        """
        Search for content by specific topic

        Args:
            topic: The topic to search for
            content_type: 'image' or 'document'

        Returns:
            List of suggested sources
        """
        suggestions = []

        # Get general sources
        if content_type == 'image':
            suggestions.extend(self._get_image_alternatives({}))
        else:
            suggestions.extend(self._get_document_alternatives({}))

        # Try specific search
        if topic:
            wikimedia_results = self._search_wikimedia(topic)
            suggestions.extend(wikimedia_results)

        return suggestions

    def get_all_open_sources(self):
        """Get complete list of open content sources"""
        return {
            'images': self.open_sources['images'],
            'documents': self.open_sources['documents']
        }


def format_alternatives_for_display(alternatives):
    """Format alternatives list for nice display"""
    formatted = []

    for alt in alternatives:
        formatted_alt = {
            'display_text': f"{alt['source']}",
            'url': alt['url'],
            'license': alt['license'],
            'description': alt.get('description', ''),
        }

        if alt.get('title'):
            formatted_alt['display_text'] += f' - {alt["title"]}'

        formatted.append(formatted_alt)

    return formatted
