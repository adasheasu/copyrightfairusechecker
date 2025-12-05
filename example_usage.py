"""
Example Usage Script
Demonstrates how to use the copyright checker modules programmatically
"""

from utils.image_analyzer import ImageAnalyzer
from utils.document_analyzer import DocumentAnalyzer
from utils.copyright_checker import CopyrightChecker
from utils.fair_use_assessor import FairUseAssessor
from utils.alternative_finder import AlternativeFinder
import json


def analyze_image_example(image_path):
    """Example: Analyze an image file"""
    print("=" * 60)
    print("ANALYZING IMAGE")
    print("=" * 60)

    # Initialize analyzers
    image_analyzer = ImageAnalyzer()
    copyright_checker = CopyrightChecker()
    fair_use_assessor = FairUseAssessor()
    alternative_finder = AlternativeFinder()

    # Analyze the image
    print(f"\n1. Analyzing image: {image_path}")
    source_info = image_analyzer.analyze(image_path)
    print(f"   - Dimensions: {source_info.get('dimensions')}")
    print(f"   - Format: {source_info.get('format')}")
    print(f"   - File size: {source_info.get('file_size')} bytes")

    # Check copyright
    print("\n2. Checking copyright...")
    copyright_info = copyright_checker.check_image(image_path)
    print(f"   - License: {copyright_info.get('license_type')}")
    print(f"   - Copyright holder: {copyright_info.get('copyright_holder')}")
    print(f"   - Commercial use: {copyright_info.get('commercial_use_allowed')}")

    # Assess fair use
    print("\n3. Assessing fair use for educational use...")
    fair_use_result = fair_use_assessor.assess(
        copyright_info,
        course_type='Online',
        institution_type='Public University',
        content_type='image'
    )
    print(f"   - Can use: {fair_use_result.get('can_use')}")
    print(f"   - Confidence: {fair_use_result.get('confidence')}")

    # Find alternatives if needed
    if fair_use_result.get('can_use') == False:
        print("\n4. Finding alternative content...")
        alternatives = alternative_finder.find_alternatives(source_info, copyright_info)
        print(f"   - Found {len(alternatives)} alternatives")
        for i, alt in enumerate(alternatives[:3], 1):
            print(f"   {i}. {alt.get('source')}: {alt.get('url')}")

    print("\n" + "=" * 60 + "\n")


def analyze_document_example(document_path):
    """Example: Analyze a document file"""
    print("=" * 60)
    print("ANALYZING DOCUMENT")
    print("=" * 60)

    # Initialize analyzers
    doc_analyzer = DocumentAnalyzer()
    copyright_checker = CopyrightChecker()
    fair_use_assessor = FairUseAssessor()

    # Analyze the document
    print(f"\n1. Analyzing document: {document_path}")
    source_info = doc_analyzer.analyze(document_path)
    print(f"   - Author: {source_info.get('author')}")
    print(f"   - Title: {source_info.get('title')}")
    print(f"   - Page count: {source_info.get('page_count')}")
    print(f"   - Copyright notices: {len(source_info.get('copyright_notices', []))}")

    # Check copyright
    print("\n2. Checking copyright...")
    copyright_info = copyright_checker.check_document(document_path)
    print(f"   - License: {copyright_info.get('license_type')}")
    print(f"   - Public domain: {copyright_info.get('is_public_domain')}")

    # Assess fair use
    print("\n3. Assessing fair use...")
    fair_use_result = fair_use_assessor.assess(
        copyright_info,
        course_type='Hybrid',
        institution_type='Community College',
        content_type='document'
    )

    print(f"   - Can use: {fair_use_result.get('can_use')}")
    print(f"   - Recommendation:")
    recommendation_lines = fair_use_result.get('recommendation', '').split('\n')
    for line in recommendation_lines[:5]:  # First 5 lines
        if line.strip():
            print(f"     {line.strip()}")

    print("\n" + "=" * 60 + "\n")


def search_alternatives_example(topic):
    """Example: Search for alternative open content by topic"""
    print("=" * 60)
    print(f"SEARCHING FOR ALTERNATIVES: {topic}")
    print("=" * 60)

    alternative_finder = AlternativeFinder()

    # Search for images
    print("\n1. Image sources:")
    image_alternatives = alternative_finder.search_by_topic(topic, content_type='image')
    for i, alt in enumerate(image_alternatives[:5], 1):
        print(f"   {i}. {alt.get('source')}")
        print(f"      URL: {alt.get('url')}")
        print(f"      License: {alt.get('license')}")

    # Search for documents
    print("\n2. Document/textbook sources:")
    doc_alternatives = alternative_finder.search_by_topic(topic, content_type='document')
    for i, alt in enumerate(doc_alternatives[:5], 1):
        print(f"   {i}. {alt.get('source')}")
        print(f"      URL: {alt.get('url')}")
        print(f"      License: {alt.get('license')}")

    print("\n" + "=" * 60 + "\n")


def check_url_license_example(url):
    """Example: Check license for a specific URL"""
    print("=" * 60)
    print(f"CHECKING URL LICENSE")
    print("=" * 60)

    copyright_checker = CopyrightChecker()

    print(f"\nURL: {url}")
    license_info = copyright_checker.check_url_license(url)

    print(f"\nResults:")
    print(f"  - Source: {license_info.get('source')}")
    print(f"  - License: {license_info.get('license_type')}")
    print(f"  - Commercial use: {license_info.get('commercial_use_allowed')}")
    print(f"  - Attribution required: {license_info.get('attribution_required')}")

    if license_info.get('note'):
        print(f"  - Note: {license_info.get('note')}")

    print("\n" + "=" * 60 + "\n")


def main():
    """
    Main function with usage examples

    Note: Replace the file paths with actual files to test
    """
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  Copyright & Fair Use Checker - Example Usage            ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\n")

    # Example 1: Analyze an image (would need an actual image file)
    # analyze_image_example('path/to/your/image.jpg')

    # Example 2: Analyze a document (would need an actual document)
    # analyze_document_example('path/to/your/document.pdf')

    # Example 3: Search for alternatives
    print("Example 1: Searching for alternative content")
    search_alternatives_example('biology cell diagram')

    # Example 4: Check URL license
    print("\nExample 2: Checking license for specific URLs")
    check_url_license_example('https://commons.wikimedia.org/wiki/File:Example.jpg')
    check_url_license_example('https://unsplash.com/photos/abc123')
    check_url_license_example('https://www.flickr.com/photos/example/12345')

    # Example 5: Get all open sources
    print("\nExample 3: Listing all available open content sources")
    print("=" * 60)
    alternative_finder = AlternativeFinder()
    all_sources = alternative_finder.get_all_open_sources()

    print("\nImage Sources:")
    for source in all_sources['images']:
        print(f"  - {source['name']}: {source['url']}")

    print("\nDocument Sources:")
    for source in all_sources['documents']:
        print(f"  - {source['name']}: {source['url']}")

    print("\n" + "=" * 60 + "\n")

    print("\n📝 Note: To test image and document analysis:")
    print("   1. Uncomment the example function calls in main()")
    print("   2. Replace the file paths with actual files")
    print("   3. Run: python3 example_usage.py")
    print("\n")


if __name__ == "__main__":
    main()
