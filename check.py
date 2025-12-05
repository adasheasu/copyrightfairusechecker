#!/usr/bin/env python3
"""
Simple Command-Line Copyright Checker
Usage: python3 check.py <file_path> [options]
"""

import sys
import argparse
from pathlib import Path
from utils.image_analyzer import ImageAnalyzer
from utils.document_analyzer import DocumentAnalyzer
from utils.copyright_checker import CopyrightChecker
from utils.fair_use_assessor import FairUseAssessor
from utils.alternative_finder import AlternativeFinder


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(title):
    """Print section title"""
    print(f"\n📋 {title}")
    print("-" * 70)


def check_file(file_path, course_type='Online', institution='Public University', show_alternatives=True):
    """
    Check a single file for copyright and fair use

    Args:
        file_path: Path to the file
        course_type: Type of course (Online, Hybrid, In-person)
        institution: Institution type
        show_alternatives: Whether to show alternative sources
    """
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    print_header(f"Copyright & Fair Use Check: {file_path.name}")

    # Determine file type
    extension = file_path.suffix.lower()
    is_image = extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    is_document = extension in ['.pdf', '.docx', '.doc', '.txt']

    if not is_image and not is_document:
        print(f"❌ Error: Unsupported file type: {extension}")
        print("   Supported: .jpg, .jpeg, .png, .gif, .pdf, .docx, .doc")
        sys.exit(1)

    # Initialize analyzers
    copyright_checker = CopyrightChecker()
    fair_use_assessor = FairUseAssessor()

    # Analyze based on file type
    print("\n🔍 Analyzing file...")

    if is_image:
        image_analyzer = ImageAnalyzer()
        source_info = image_analyzer.analyze(str(file_path))
        copyright_info = copyright_checker.check_image(str(file_path))
        content_type = 'image'

        # Display image info
        print_section("Image Information")
        if source_info.get('dimensions'):
            print(f"   Dimensions: {source_info['dimensions']}")
        if source_info.get('format'):
            print(f"   Format: {source_info['format']}")
        if source_info.get('file_size'):
            size_kb = source_info['file_size'] / 1024
            print(f"   Size: {size_kb:.2f} KB")

    else:  # Document
        doc_analyzer = DocumentAnalyzer()
        source_info = doc_analyzer.analyze(str(file_path))
        copyright_info = copyright_checker.check_document(str(file_path))
        content_type = 'document'

        # Display document info
        print_section("Document Information")
        if source_info.get('author'):
            print(f"   Author: {source_info['author']}")
        if source_info.get('title'):
            print(f"   Title: {source_info['title']}")
        if source_info.get('page_count'):
            print(f"   Pages: {source_info['page_count']}")

    # Display copyright information
    print_section("Copyright & License")

    license_type = copyright_info.get('license_type', 'Unknown')
    print(f"   License: {license_type}")

    if copyright_info.get('copyright_holder'):
        print(f"   Copyright Holder: {copyright_info['copyright_holder']}")

    if copyright_info.get('year'):
        print(f"   Year: {copyright_info['year']}")

    if copyright_info.get('is_public_domain'):
        print(f"   ✅ Public Domain: Yes")

    if copyright_info.get('commercial_use_allowed') is not None:
        status = "Yes" if copyright_info['commercial_use_allowed'] else "No"
        print(f"   Commercial Use: {status}")

    if copyright_info.get('modifications_allowed') is not None:
        status = "Yes" if copyright_info['modifications_allowed'] else "No"
        print(f"   Modifications: {status}")

    if copyright_info.get('attribution_required'):
        print(f"   ⚠️  Attribution Required: Yes")
        if copyright_info.get('attribution_text'):
            print(f"\n   Attribution text:")
            print(f"   \"{copyright_info['attribution_text']}\"")

    # Display restrictions
    if copyright_info.get('restrictions'):
        print(f"\n   Restrictions:")
        for restriction in copyright_info['restrictions']:
            print(f"   • {restriction}")

    # Fair use assessment
    print_section("Fair Use Assessment for Educational Use")
    print(f"   Course Type: {course_type}")
    print(f"   Institution: {institution}")

    fair_use_result = fair_use_assessor.assess(
        copyright_info,
        course_type,
        institution,
        content_type
    )

    # Display result
    can_use = fair_use_result.get('can_use')
    confidence = fair_use_result.get('confidence', 'Unknown')

    print()
    if can_use is True:
        print(f"   ✅ CAN USE - Confidence: {confidence}")
        print(f"   This content appears to be usable in your course.")
    elif can_use is False:
        print(f"   ❌ CANNOT USE - Confidence: {confidence}")
        print(f"   This content may not be usable due to copyright restrictions.")
    else:
        print(f"   ⚠️  NEEDS REVIEW - Confidence: {confidence}")
        print(f"   Manual review recommended.")

    # Display four factors
    if fair_use_result.get('factors'):
        print(f"\n   Four-Factor Analysis:")
        factors = fair_use_result['factors']
        for factor_name, factor_desc in factors.items():
            print(f"   • {factor_desc}")

    # Display recommendation
    if fair_use_result.get('recommendation'):
        print(f"\n   Recommendation:")
        lines = fair_use_result['recommendation'].split('\n')
        for line in lines[:10]:  # First 10 lines
            if line.strip():
                print(f"   {line.strip()}")

    # Best practices
    if fair_use_result.get('best_practices'):
        print(f"\n   Best Practices:")
        for practice in fair_use_result['best_practices'][:5]:  # First 5
            print(f"   • {practice}")

    # Show alternatives if content cannot be used
    if show_alternatives and (can_use == False or copyright_info.get('restrictions')):
        print_section("Alternative Content Sources")

        alternative_finder = AlternativeFinder()
        alternatives = alternative_finder.find_alternatives(source_info, copyright_info)

        if alternatives:
            print(f"\n   Found {len(alternatives)} alternative sources:\n")
            for i, alt in enumerate(alternatives[:8], 1):  # Show top 8
                print(f"   {i}. {alt.get('source', 'Unknown')}")
                if alt.get('url'):
                    print(f"      URL: {alt['url']}")
                if alt.get('license'):
                    print(f"      License: {alt['license']}")
                if alt.get('description'):
                    print(f"      {alt['description']}")
                print()
        else:
            print("   No specific alternatives found. Visit these sources:")
            print("   • Wikimedia Commons: https://commons.wikimedia.org")
            print("   • Unsplash: https://unsplash.com")
            print("   • OpenStax: https://openstax.org")

    # Summary
    print("\n" + "=" * 70)
    if can_use is True:
        print("  ✅ SUMMARY: Content appears usable with proper attribution")
    elif can_use is False:
        print("  ❌ SUMMARY: Seek alternatives or permission")
    else:
        print("  ⚠️  SUMMARY: Consult your copyright office")
    print("=" * 70 + "\n")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Check copyright and fair use for educational content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 check.py myimage.jpg
  python3 check.py document.pdf --course Online --institution "Community College"
  python3 check.py photo.png --no-alternatives
        """
    )

    parser.add_argument(
        'file',
        help='Path to the image or document file to check'
    )

    parser.add_argument(
        '--course',
        default='Online',
        choices=['Online', 'Hybrid', 'In-person'],
        help='Course type (default: Online)'
    )

    parser.add_argument(
        '--institution',
        default='Public University',
        choices=['Public University', 'Private University', 'Community College', 'K-12'],
        help='Institution type (default: Public University)'
    )

    parser.add_argument(
        '--no-alternatives',
        action='store_true',
        help='Do not show alternative content sources'
    )

    args = parser.parse_args()

    # Check the file
    check_file(
        args.file,
        course_type=args.course,
        institution=args.institution,
        show_alternatives=not args.no_alternatives
    )


if __name__ == "__main__":
    main()
