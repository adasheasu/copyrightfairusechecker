# Copyright & Fair Use Checker for Educational Content

A comprehensive web-based tool to help educators identify images and written materials, check their copyright status, assess fair use for educational purposes, and find alternative openly-licensed content.

## Features

### 🔍 Content Analysis
- **Image Analysis**: Reverse image search, metadata extraction, EXIF data reading
- **Document Analysis**: Text extraction from PDFs and Word documents, metadata parsing
- **Source Identification**: Attempts to identify original sources and creators

### ©️ Copyright Detection
- **License Identification**: Detects Creative Commons licenses, Public Domain, and other open licenses
- **Copyright Notices**: Extracts copyright information from metadata and content
- **Attribution Requirements**: Identifies when attribution is required and generates proper attribution text

### ⚖️ Fair Use Assessment
- **Four-Factor Analysis**: Evaluates fair use based on:
  1. Purpose and character of use
  2. Nature of the copyrighted work
  3. Amount and substantiality used
  4. Effect on market value
- **Educational Context**: Considers course type, institution type, and distribution method
- **Risk Assessment**: Provides confidence levels and recommendations

### 🔄 Alternative Content Finder
- **Open Source Databases**: Suggests alternatives from:
  - Wikimedia Commons
  - Unsplash, Pexels, Pixabay
  - OpenStax, Open Textbook Library
  - NASA, Smithsonian, Library of Congress
  - And many more...
- **Automatic Search**: Searches for similar openly-licensed content
- **Educational Resources**: Prioritizes sources designed for educational use

### 📦 Batch Processing
- Analyze multiple files simultaneously
- Summary statistics and detailed reports
- Export results for documentation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   cd copyright-checker
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the tool**
   - The application will open in your default browser
   - Default URL: http://localhost:8501

## Usage Guide

### Single File Analysis

1. Select **"Single File"** mode in the sidebar
2. Upload an image (JPG, PNG, GIF) or document (PDF, DOCX)
3. Configure analysis options:
   - Reverse Image Search
   - Copyright Detection
   - Fair Use Assessment
   - Find Alternatives
4. Set your context:
   - Course Type (Online, Hybrid, In-person)
   - Institution Type
5. View results including:
   - Source information
   - Copyright and licensing details
   - Fair use assessment with four-factor analysis
   - Alternative content suggestions

### Batch Processing

1. Select **"Batch Processing"** mode in the sidebar
2. Upload multiple files
3. Configure analysis options (same as single file)
4. View summary statistics:
   - Total files processed
   - Usable vs. not usable count
   - Files requiring manual review
5. Expand individual files for detailed analysis

## Understanding the Results

### Can Use Status

- ✅ **Usable**: Content appears safe to use based on license or fair use analysis
- ❌ **Not Usable**: Copyright restrictions likely prevent use; seek alternatives or permission
- ⚠️ **Needs Review**: Unclear status; manual review and legal consultation recommended

### Fair Use Assessment

The tool evaluates four factors required by US copyright law:

1. **Purpose & Character**: Educational, nonprofit use favors fair use
2. **Nature of Work**: Factual works favor fair use more than creative works
3. **Amount Used**: Using less of the work favors fair use
4. **Market Effect**: No negative market impact favors fair use

### License Types

- **Public Domain**: Free to use without restrictions
- **Creative Commons (CC)**: Open licenses with varying restrictions
  - CC0: Public domain dedication
  - CC BY: Requires attribution
  - CC BY-SA: Requires attribution and share-alike
  - CC BY-NC: Non-commercial use only
  - CC BY-ND: No derivatives allowed
- **All Rights Reserved**: Full copyright protection; requires permission

## Best Practices for Educational Use

### Always:
1. ✅ Provide proper attribution to creators
2. ✅ Use only what's necessary for educational purposes
3. ✅ Limit access to enrolled students (password-protect in LMS)
4. ✅ Include copyright disclaimers
5. ✅ Document your fair use reasoning
6. ✅ Review usage annually

### Never:
1. ❌ Make content publicly accessible outside your course
2. ❌ Use entire works when excerpts would suffice
3. ❌ Ignore license restrictions
4. ❌ Assume "educational use" means unlimited use
5. ❌ Republish or redistribute openly-licensed content without proper attribution

### For Online Courses:
- Use learning management system (Canvas, Blackboard, etc.)
- Enable password protection and access controls
- Consider time-limited access (remove at end of term)
- Add copyright notices to each page/screen
- Avoid downloadable versions when possible

## Important Legal Disclaimer

**This tool provides guidance only and does not constitute legal advice.**

- Fair use is determined on a case-by-case basis by courts
- The tool's assessments are based on general principles but cannot predict legal outcomes
- When in doubt, consult your institution's legal counsel or copyright office
- Always err on the side of caution and seek permission when uncertain

## Technical Details

### Supported File Formats
- **Images**: JPG, JPEG, PNG, GIF
- **Documents**: PDF, DOCX, DOC

### Data Processing
- All processing happens locally on your machine
- No files are uploaded to external servers (except for optional API calls)
- Temporary files are deleted after analysis

### API Integration (Optional)

For enhanced functionality, you can integrate with:
- **Google Cloud Vision API**: Advanced reverse image search
- **TinEye API**: Commercial reverse image search
- **Bing Visual Search API**: Alternative reverse image search

To enable API features, add your API keys to a `.env` file:
```
GOOGLE_VISION_API_KEY=your_key_here
TINEYE_API_KEY=your_key_here
```

## Troubleshooting

### Common Issues

**Issue**: "Module not found" error
- **Solution**: Make sure you've installed all requirements: `pip install -r requirements.txt`

**Issue**: PDF analysis fails
- **Solution**: Install PyPDF2: `pip install PyPDF2`

**Issue**: Word document analysis fails
- **Solution**: Install python-docx: `pip install python-docx`

**Issue**: Application won't start
- **Solution**: Check that port 8501 is not in use. Use a different port: `streamlit run app.py --server.port 8502`

## Resources

### Copyright and Fair Use
- [US Copyright Office - Fair Use](https://www.copyright.gov/fair-use/)
- [Stanford Copyright & Fair Use Center](https://fairuse.stanford.edu/)
- [TEACH Act Guide](https://www.copyright.gov/legislation/dmca.pdf)

### Open Educational Resources
- [OER Commons](https://www.oercommons.org)
- [MERLOT](https://www.merlot.org)
- [Creative Commons](https://creativecommons.org)

### Institutional Resources
- Contact your institution's copyright office
- Consult your library's copyright specialist
- Review your institution's fair use guidelines

## Contributing

Suggestions and improvements are welcome! This tool is designed to be extended with additional features such as:
- Video content analysis
- Audio content analysis
- Integration with institutional repositories
- Custom institutional policies
- Enhanced API integrations

## Version

**Version 1.0**
- Initial release with core functionality
- Single file and batch processing
- Fair use assessment
- Alternative content finder

## License

This tool itself is released under the MIT License. However, please note that using this tool to analyze copyrighted content does not grant you any rights to that content.

---

**Created for educational institutions to promote proper use of copyrighted materials and discovery of open educational resources.**
