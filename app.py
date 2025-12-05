"""
Copyright and Fair Use Checker for Educational Content
A tool to identify images and written materials, check their copyright status,
and determine if they can be used in online college courses.
"""

import streamlit as st
import os
from pathlib import Path
from utils.image_analyzer import ImageAnalyzer
from utils.document_analyzer import DocumentAnalyzer
from utils.copyright_checker import CopyrightChecker
from utils.fair_use_assessor import FairUseAssessor
from utils.alternative_finder import AlternativeFinder

# Page configuration
st.set_page_config(
    page_title="Copyright & Fair Use Checker",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

def main():
    st.title("📚 Copyright & Fair Use Checker for Educational Content")
    st.markdown("""
    Upload images or documents to:
    - Identify original sources
    - Check copyright and licensing
    - Assess fair use for educational purposes
    - Get alternative suggestions if content isn't usable
    """)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        analysis_mode = st.radio(
            "Analysis Mode",
            ["Single File", "Batch Processing"],
            help="Choose whether to analyze one file or multiple files"
        )

        st.divider()

        st.subheader("Analysis Options")
        check_reverse_image = st.checkbox("Reverse Image Search", value=True)
        check_copyright = st.checkbox("Copyright Detection", value=True)
        check_fair_use = st.checkbox("Fair Use Assessment", value=True)
        find_alternatives = st.checkbox("Find Alternatives", value=True)

        st.divider()

        st.subheader("Context")
        course_type = st.selectbox(
            "Course Type",
            ["Online", "Hybrid", "In-person"],
            help="Where will this content be used?"
        )

        institution_type = st.selectbox(
            "Institution",
            ["Public University", "Private University", "Community College", "K-12"],
            help="Type of educational institution"
        )

    # Main content area
    if analysis_mode == "Single File":
        uploaded_file = st.file_uploader(
            "Upload a file to analyze",
            type=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'docx', 'doc'],
            help="Supported formats: Images (JPG, PNG, GIF) and Documents (PDF, DOCX)"
        )

        if uploaded_file is not None:
            analyze_single_file(
                uploaded_file,
                check_reverse_image,
                check_copyright,
                check_fair_use,
                find_alternatives,
                course_type,
                institution_type
            )

    else:  # Batch Processing
        uploaded_files = st.file_uploader(
            "Upload multiple files to analyze",
            type=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            help="Supported formats: Images (JPG, PNG, GIF) and Documents (PDF, DOCX)"
        )

        if uploaded_files:
            analyze_batch_files(
                uploaded_files,
                check_reverse_image,
                check_copyright,
                check_fair_use,
                find_alternatives,
                course_type,
                institution_type
            )

def analyze_single_file(file, reverse_image, copyright_check, fair_use, alternatives, course_type, institution):
    """Analyze a single uploaded file"""

    # Save file temporarily
    temp_dir = Path("data/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / file.name

    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())

    # Display file
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📄 Uploaded File")
        file_extension = file.name.split('.')[-1].lower()

        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            st.image(str(temp_path), caption=file.name, use_container_width=True)
        else:
            st.info(f"📄 {file.name}\n\nType: {file_extension.upper()}\nSize: {file.size / 1024:.2f} KB")

    with col2:
        st.subheader("🔍 Analysis Results")

        with st.spinner("Analyzing file..."):
            results = perform_analysis(
                temp_path,
                file_extension,
                reverse_image,
                copyright_check,
                fair_use,
                alternatives,
                course_type,
                institution
            )

            display_results(results, file.name)

    # Clean up
    if temp_path.exists():
        temp_path.unlink()

def analyze_batch_files(files, reverse_image, copyright_check, fair_use, alternatives, course_type, institution):
    """Analyze multiple uploaded files"""

    st.subheader(f"📦 Batch Analysis ({len(files)} files)")

    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    results_list = []

    for idx, file in enumerate(files):
        status_text.text(f"Processing {idx + 1}/{len(files)}: {file.name}")

        # Save file temporarily
        temp_dir = Path("data/temp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / file.name

        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())

        file_extension = file.name.split('.')[-1].lower()

        # Analyze
        results = perform_analysis(
            temp_path,
            file_extension,
            reverse_image,
            copyright_check,
            fair_use,
            alternatives,
            course_type,
            institution
        )

        results['filename'] = file.name
        results_list.append(results)

        # Clean up
        if temp_path.exists():
            temp_path.unlink()

        # Update progress
        progress_bar.progress((idx + 1) / len(files))

    status_text.text("✅ Analysis complete!")

    # Display batch results
    display_batch_results(results_list)

def perform_analysis(file_path, file_type, reverse_image, copyright_check, fair_use, alternatives, course_type, institution):
    """Perform the actual analysis on a file"""

    results = {
        'file_type': file_type,
        'source_info': None,
        'copyright_info': None,
        'fair_use_assessment': None,
        'alternatives': None,
        'can_use': None,
        'warnings': []
    }

    try:
        # Image analysis
        if file_type in ['jpg', 'jpeg', 'png', 'gif']:
            if reverse_image:
                image_analyzer = ImageAnalyzer()
                results['source_info'] = image_analyzer.analyze(file_path)

            if copyright_check:
                copyright_checker = CopyrightChecker()
                results['copyright_info'] = copyright_checker.check_image(file_path)

        # Document analysis
        elif file_type in ['pdf', 'docx', 'doc']:
            doc_analyzer = DocumentAnalyzer()
            results['source_info'] = doc_analyzer.analyze(file_path)

            if copyright_check:
                copyright_checker = CopyrightChecker()
                results['copyright_info'] = copyright_checker.check_document(file_path)

        # Fair use assessment
        if fair_use and results['copyright_info']:
            assessor = FairUseAssessor()
            results['fair_use_assessment'] = assessor.assess(
                results['copyright_info'],
                course_type,
                institution,
                file_type
            )
            results['can_use'] = results['fair_use_assessment']['can_use']

        # Find alternatives if needed
        if alternatives and (results['can_use'] == False or results.get('warnings')):
            finder = AlternativeFinder()
            results['alternatives'] = finder.find_alternatives(
                results['source_info'],
                results['copyright_info']
            )

    except Exception as e:
        results['warnings'].append(f"Error during analysis: {str(e)}")

    return results

def display_results(results, filename):
    """Display analysis results for a single file"""

    # Overall status
    if results['can_use'] is True:
        st.success("✅ This content appears to be usable in your course")
    elif results['can_use'] is False:
        st.error("❌ This content may not be usable due to copyright restrictions")
    else:
        st.warning("⚠️ Unable to determine usability - manual review recommended")

    # Source Information
    if results['source_info']:
        with st.expander("🔎 Source Information", expanded=True):
            source = results['source_info']
            if source.get('original_url'):
                st.write(f"**Original Source:** {source['original_url']}")
            if source.get('author'):
                st.write(f"**Author/Creator:** {source['author']}")
            if source.get('title'):
                st.write(f"**Title:** {source['title']}")
            if source.get('date'):
                st.write(f"**Date:** {source['date']}")
            if source.get('confidence'):
                st.write(f"**Confidence:** {source['confidence']}")

    # Copyright Information
    if results['copyright_info']:
        with st.expander("©️ Copyright & Licensing", expanded=True):
            copyright_info = results['copyright_info']

            if copyright_info.get('license_type'):
                license_type = copyright_info['license_type']
                if 'Creative Commons' in license_type or 'Public Domain' in license_type:
                    st.success(f"**License:** {license_type}")
                else:
                    st.warning(f"**License:** {license_type}")

            if copyright_info.get('copyright_holder'):
                st.write(f"**Copyright Holder:** {copyright_info['copyright_holder']}")

            if copyright_info.get('restrictions'):
                st.write("**Restrictions:**")
                for restriction in copyright_info['restrictions']:
                    st.write(f"- {restriction}")

            if copyright_info.get('attribution_required'):
                st.info("ℹ️ **Attribution Required**")
                if copyright_info.get('attribution_text'):
                    st.code(copyright_info['attribution_text'])

    # Fair Use Assessment
    if results['fair_use_assessment']:
        with st.expander("⚖️ Fair Use Assessment", expanded=True):
            assessment = results['fair_use_assessment']

            st.write("**Four Factors Analysis:**")
            factors = assessment.get('factors', {})

            col1, col2 = st.columns(2)
            with col1:
                st.write("**1. Purpose & Character**")
                st.write(factors.get('purpose', 'Not assessed'))
                st.write("")
                st.write("**2. Nature of Work**")
                st.write(factors.get('nature', 'Not assessed'))

            with col2:
                st.write("**3. Amount Used**")
                st.write(factors.get('amount', 'Not assessed'))
                st.write("")
                st.write("**4. Market Effect**")
                st.write(factors.get('market_effect', 'Not assessed'))

            st.divider()

            if assessment.get('recommendation'):
                st.write("**Recommendation:**")
                st.write(assessment['recommendation'])

    # Alternatives
    if results['alternatives']:
        with st.expander("🔄 Alternative Content Suggestions", expanded=results['can_use'] == False):
            alternatives = results['alternatives']

            for idx, alt in enumerate(alternatives, 1):
                st.write(f"**Option {idx}:**")
                if alt.get('source'):
                    st.write(f"- **Source:** {alt['source']}")
                if alt.get('url'):
                    st.write(f"- **URL:** [{alt['url']}]({alt['url']})")
                if alt.get('license'):
                    st.write(f"- **License:** {alt['license']}")
                if alt.get('description'):
                    st.write(f"- **Description:** {alt['description']}")
                st.divider()

    # Warnings
    if results['warnings']:
        with st.expander("⚠️ Warnings & Notes"):
            for warning in results['warnings']:
                st.warning(warning)

def display_batch_results(results_list):
    """Display results for batch processing"""

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)

    usable = sum(1 for r in results_list if r['can_use'] is True)
    not_usable = sum(1 for r in results_list if r['can_use'] is False)
    unknown = sum(1 for r in results_list if r['can_use'] is None)

    col1.metric("Total Files", len(results_list))
    col2.metric("✅ Usable", usable)
    col3.metric("❌ Not Usable", not_usable)
    col4.metric("⚠️ Needs Review", unknown)

    st.divider()

    # Detailed results table
    st.subheader("Detailed Results")

    for result in results_list:
        filename = result.get('filename', 'Unknown')
        can_use = result.get('can_use')

        if can_use is True:
            status_icon = "✅"
            status_text = "Usable"
        elif can_use is False:
            status_icon = "❌"
            status_text = "Not Usable"
        else:
            status_icon = "⚠️"
            status_text = "Review Needed"

        with st.expander(f"{status_icon} {filename} - {status_text}"):
            display_results(result, filename)

if __name__ == "__main__":
    main()
