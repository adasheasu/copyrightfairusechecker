# Usage Guide - Copyright & Fair Use Checker

This tool provides **three different interfaces** to check copyright and assess fair use. Choose the one that best fits your needs!

---

## 🖥️ Method 1: Command-Line Interface (Fastest)

Perfect for quickly checking a single file from the terminal.

### Installation
```bash
cd /Users/alejandradashe/copyright-checker
pip3 install -r requirements.txt
```

### Basic Usage

**Check an image:**
```bash
python3 check.py myimage.jpg
```

**Check a PDF document:**
```bash
python3 check.py document.pdf
```

**Check with custom settings:**
```bash
python3 check.py photo.png --course Hybrid --institution "Community College"
```

**Skip alternatives (faster):**
```bash
python3 check.py image.jpg --no-alternatives
```

### Command Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--course` | Online, Hybrid, In-person | Online | Your course type |
| `--institution` | Public University, Private University, Community College, K-12 | Public University | Your institution |
| `--no-alternatives` | flag | false | Skip finding alternatives |

### Example Output

```
======================================================================
  Copyright & Fair Use Check: sample.jpg
======================================================================

🔍 Analyzing file...

📋 Image Information
----------------------------------------------------------------------
   Dimensions: 1920x1080
   Format: JPEG
   Size: 245.32 KB

©️ Copyright & License
----------------------------------------------------------------------
   License: Creative Commons Attribution
   Attribution Required: Yes
   ...

⚖️ Fair Use Assessment for Educational Use
----------------------------------------------------------------------
   Course Type: Online
   Institution: Public University

   ✅ CAN USE - Confidence: High
   This content appears to be usable in your course.
   ...
```

---

## 🌐 Method 2: HTML Web Interface (Easiest)

Beautiful, user-friendly web interface. Perfect for non-technical users!

### Start the Server

```bash
cd /Users/alejandradashe/copyright-checker
python3 server.py
```

The server will start and display:
```
======================================================================
  Copyright & Fair Use Checker - Web Interface
======================================================================

  Starting server...
  Open your browser to: http://localhost:5000

  Press Ctrl+C to stop the server

======================================================================
```

### Using the Interface

1. **Open your browser** to `http://localhost:5000`

2. **Upload a file**:
   - Click the upload area, OR
   - Drag and drop your file

3. **Configure settings**:
   - Select your course type
   - Select your institution

4. **Click "Check Copyright & Fair Use"**

5. **View beautiful results**:
   - ✅ Green = Can use
   - ❌ Red = Cannot use
   - ⚠️ Yellow = Needs review

6. **Review details**:
   - Copyright information
   - Four-factor analysis
   - Recommendations
   - Alternative sources (if needed)

### Features

- 📱 **Mobile-friendly** - Works on phones and tablets
- 🎨 **Beautiful design** - Modern, gradient interface
- 🖱️ **Drag & drop** - Easy file upload
- 📊 **Visual results** - Color-coded status indicators
- 🔗 **Clickable links** - Direct links to alternative sources

### Supported Files

- **Images**: JPG, JPEG, PNG, GIF
- **Documents**: PDF, DOCX, DOC
- **Max size**: 16MB per file

---

## 📊 Method 3: Streamlit Web App (Feature-Rich)

Full-featured web app with batch processing and advanced features.

### Start Streamlit

```bash
cd /Users/alejandradashe/copyright-checker
streamlit run app.py
```

### Features

- **Single file mode** - Analyze one file at a time
- **Batch processing** - Upload and analyze multiple files
- **Summary statistics** - See overall results for batches
- **Expandable sections** - Detailed information on demand
- **Export results** - Save analysis for documentation

### When to Use Streamlit

- Need to process many files at once
- Want detailed analysis with all sections
- Need to export results
- Prefer more technical interface

---

## 🎯 Which Interface Should You Use?

| Interface | Best For | Pros | Cons |
|-----------|----------|------|------|
| **Command-Line** | Quick checks, automation, tech users | Fastest, scriptable | Terminal only, no visuals |
| **HTML (Flask)** | Non-tech users, presentations | Beautiful, easy, mobile-friendly | Single file only |
| **Streamlit** | Batch processing, detailed analysis | Most features, batch mode | More complex, slower |

---

## 📝 Example Workflows

### Workflow 1: Quick Single File Check

**Goal**: Check one image quickly

**Use**: Command-line
```bash
python3 check.py ~/Downloads/diagram.png
```

**Time**: ~5 seconds

---

### Workflow 2: Check Multiple Course Materials

**Goal**: Check 20 images and PDFs for your course

**Use**: Streamlit
```bash
streamlit run app.py
```
1. Select "Batch Processing"
2. Upload all 20 files
3. Review summary statistics
4. Expand files that need attention

**Time**: ~2 minutes

---

### Workflow 3: Present to Faculty

**Goal**: Show colleagues how to check copyright

**Use**: HTML Interface
```bash
python3 server.py
```
1. Open http://localhost:5000 on projector
2. Drag and drop example file
3. Show beautiful results
4. Demonstrate alternative sources

**Time**: Great for demos!

---

### Workflow 4: Automate Checks

**Goal**: Check all images in a folder

**Use**: Command-line with script
```bash
#!/bin/bash
for file in ~/course-materials/images/*; do
    python3 check.py "$file" --course Online >> results.txt
done
```

**Time**: Automated!

---

## 💡 Tips & Tricks

### Command-Line Tips

1. **Create an alias** for quick access:
   ```bash
   echo 'alias copyright-check="python3 ~/copyright-checker/check.py"' >> ~/.zshrc
   source ~/.zshrc

   # Now use anywhere:
   copyright-check ~/Downloads/image.jpg
   ```

2. **Save results to file**:
   ```bash
   python3 check.py image.jpg > results.txt
   ```

3. **Check multiple files**:
   ```bash
   for f in *.jpg; do python3 check.py "$f"; done
   ```

### HTML Interface Tips

1. **Bookmark the URL**: `http://localhost:5000`

2. **Keep server running**: Run in background
   ```bash
   python3 server.py &
   ```

3. **Access from other devices**: Change to `0.0.0.0`
   ```python
   # In server.py, change last line to:
   app.run(host='0.0.0.0', debug=True, port=5000)
   ```

### Streamlit Tips

1. **Keep streamlit running**: Use screen or tmux
   ```bash
   screen -S copyright
   streamlit run app.py
   # Ctrl+A, D to detach
   ```

2. **Change port** if 8501 is busy:
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

## 🐛 Troubleshooting

### Command-Line Issues

**Problem**: `python3: command not found`
```bash
# Try:
python check.py myfile.jpg
```

**Problem**: `Module not found`
```bash
pip3 install -r requirements.txt
```

### HTML Interface Issues

**Problem**: "Address already in use"
```bash
# Use different port:
# Edit server.py, change last line:
app.run(debug=True, port=5001)  # Use 5001 instead
```

**Problem**: Can't access from other computers
```bash
# Edit server.py, change last line:
app.run(host='0.0.0.0', debug=True, port=5000)
```

### Streamlit Issues

**Problem**: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

**Problem**: Slow performance
- Use command-line for single files
- Use HTML interface for simple checks
- Streamlit is best for batch processing

---

## 🚀 Quick Reference

### Start Command-Line
```bash
python3 check.py <file>
```

### Start HTML Interface
```bash
python3 server.py
# Open: http://localhost:5000
```

### Start Streamlit
```bash
streamlit run app.py
# Opens automatically
```

### Stop Servers
Press `Ctrl+C` in the terminal

---

## 📚 Next Steps

- Read [README.md](README.md) for detailed information
- Check [QUICKSTART.md](QUICKSTART.md) for getting started
- View [example_usage.py](example_usage.py) for programmatic use

---

**Need Help?**
- Command-line: `python3 check.py --help`
- Issues: Check documentation or contact support
- Legal advice: Consult your institution's copyright office
