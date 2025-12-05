# Quick Start Guide

Get started with the Copyright & Fair Use Checker in 5 minutes!

## Installation

```bash
# Navigate to the project directory
cd copyright-checker

# Install dependencies
pip3 install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## Your First Analysis

### Step 1: Choose Your Mode
- **Single File**: Analyze one file at a time
- **Batch Processing**: Analyze multiple files simultaneously

### Step 2: Configure Settings (Sidebar)

Check which analyses you want to perform:
- ✅ Reverse Image Search
- ✅ Copyright Detection
- ✅ Fair Use Assessment
- ✅ Find Alternatives

Set your context:
- **Course Type**: Online / Hybrid / In-person
- **Institution**: Public University / Private University / Community College / K-12

### Step 3: Upload Your Content

Drag and drop or click to upload:
- **Images**: JPG, PNG, GIF
- **Documents**: PDF, DOCX

### Step 4: Review Results

The tool will show you:

#### ✅ Can Use
- Content is safe to use (public domain or open license, or likely fair use)
- Follow the attribution and usage guidelines provided

#### ❌ Cannot Use
- Copyright restrictions apply
- Check the "Alternative Content Suggestions" section
- Consider seeking permission or using suggested alternatives

#### ⚠️ Needs Review
- Status unclear
- Review the fair use assessment details
- Consider consulting your institution's copyright office

## Example Scenarios

### Scenario 1: Course Textbook Image

You want to use an image from a textbook in your online course:

1. Upload the image
2. Set Course Type: "Online"
3. Set Institution: "Public University"
4. Review the fair use assessment
5. If ❌, check alternatives from open sources

### Scenario 2: Finding Open Content

You need diagrams for your biology course:

1. Check the "Alternative Content Suggestions"
2. Visit recommended sources:
   - Wikimedia Commons
   - NASA Image Gallery
   - Smithsonian Open Access
3. Download openly-licensed content
4. Use attribution text provided by the tool

### Scenario 3: Batch Checking Course Materials

You're migrating a course to a new platform:

1. Select "Batch Processing"
2. Upload all your images and PDFs
3. Review the summary:
   - How many are usable?
   - How many need alternatives?
4. Expand each file for detailed guidance

## Understanding Fair Use

The tool evaluates four factors:

### 1️⃣ Purpose & Character
- Educational, nonprofit use: ✓ Favors fair use
- Commercial use: ✗ Does not favor fair use

### 2️⃣ Nature of Work
- Factual content (data, news): ✓ Favors fair use
- Creative content (art, novels): ~ Less favorable

### 3️⃣ Amount Used
- Brief excerpts: ✓ Favors fair use
- Entire work: ~ Depends on context

### 4️⃣ Market Effect
- Doesn't replace purchase: ✓ Favors fair use
- Reduces sales: ✗ Does not favor fair use

## Best Practices Checklist

Before using any content in your course:

- [ ] Check copyright status with this tool
- [ ] Prefer openly-licensed content when available
- [ ] Always provide attribution
- [ ] Limit access to enrolled students only
- [ ] Use password-protected LMS (Canvas, Blackboard, etc.)
- [ ] Include copyright disclaimer
- [ ] Document your fair use reasoning
- [ ] Review usage annually

## Tips for Success

### For Online Courses
- Fair use is more restrictive for online courses
- Use LMS features to restrict access
- Consider time-limited access (remove after semester)
- Avoid making content downloadable

### For Finding Alternatives
- Start with the suggested open sources
- Search multiple repositories
- Look for content with CC BY license (easiest to use)
- NASA, Smithsonian, and government sources are often public domain

### When in Doubt
- Consult your institution's copyright office
- Seek permission from the copyright holder
- Use licensed content through your library
- Create your own original content

## Recommended Open Content Sources

### For Images
1. **Wikimedia Commons** - Largest collection of free media
2. **Unsplash** - High-quality photography
3. **Pexels** - Free stock photos
4. **NASA Image Gallery** - Space and science imagery
5. **Smithsonian Open Access** - Museum collections

### For Documents & Textbooks
1. **OpenStax** - Free textbooks for college courses
2. **Open Textbook Library** - Peer-reviewed textbooks
3. **MIT OpenCourseWare** - Course materials from MIT
4. **OER Commons** - Wide variety of educational resources
5. **Project Gutenberg** - Classic literature (public domain)

## Troubleshooting

### Problem: "Module not found" error
**Solution**: Run `pip3 install -r requirements.txt`

### Problem: Can't determine copyright status
**Solution**: The tool works best with:
- Images with EXIF metadata
- Documents with embedded copyright notices
- For unclear cases, err on the side of caution

### Problem: No reverse image search results
**Solution**:
- Reverse search requires internet connection
- API integration needed for enhanced results
- Manual reverse search: use Google Images or TinEye

## Need Help?

- Read the full [README.md](README.md) for detailed information
- Contact your institution's copyright office
- Consult copyright resources:
  - [Copyright.gov](https://www.copyright.gov)
  - [Stanford Fair Use](https://fairuse.stanford.edu/)
  - [Creative Commons](https://creativecommons.org)

## Important Reminder

**This tool provides guidance, not legal advice.**

Fair use is determined case-by-case by courts. When uncertain:
1. Seek permission
2. Use openly-licensed alternatives
3. Consult legal counsel

---

Happy teaching with properly licensed content! 📚
