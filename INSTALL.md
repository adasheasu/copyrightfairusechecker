# Installation Guide - Copyright & Fair Use Checker

Complete installation instructions to get the tool running on your Mac.

---

## 🚀 Quick Install (Recommended)

Follow these steps to install everything:

### Step 1: Navigate to the Project

```bash
cd /Users/alejandradashe/copyright-checker
```

### Step 2: Install All Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 3: Fix PATH (For Streamlit)

Add this line to your shell configuration file:

```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Note:** If you use bash instead of zsh, replace `~/.zshrc` with `~/.bash_profile`

---

## ✅ Verify Installation

After installation, verify everything works:

### Test Command-Line Interface
```bash
python3 check.py --help
```
Should show help message ✓

### Test HTML Interface
```bash
python3 server.py
```
Should start server ✓ (Press Ctrl+C to stop)

### Test Streamlit
```bash
streamlit run app.py
```
Should open browser ✓ (Press Ctrl+C to stop)

---

## 🔧 Alternative Methods (If Quick Install Doesn't Work)

### Method 1: Run Streamlit with Python Module

Instead of `streamlit run app.py`, use:

```bash
python3 -m streamlit run app.py
```

This bypasses the PATH issue entirely!

### Method 2: Run HTML Interface (No Streamlit Needed)

The HTML interface is simpler and doesn't need Streamlit:

```bash
python3 server.py
```

Then open: http://localhost:5000

### Method 3: Use Command-Line Only

The command-line interface works without any special setup:

```bash
python3 check.py myimage.jpg
```

---

## 📋 Complete Step-by-Step Installation

### For macOS (Your System)

1. **Open Terminal**

2. **Navigate to project folder**
   ```bash
   cd /Users/alejandradashe/copyright-checker
   ```

3. **Install dependencies**
   ```bash
   pip3 install --user -r requirements.txt
   ```

   You should see:
   ```
   Successfully installed streamlit-X.X.X flask-X.X.X ...
   ```

4. **Add Python bin to PATH**

   **If you use zsh (default on macOS Catalina+):**
   ```bash
   echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

   **If you use bash:**
   ```bash
   echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.bash_profile
   source ~/.bash_profile
   ```

5. **Verify streamlit works**
   ```bash
   streamlit --version
   ```

   Should show: `Streamlit, version X.X.X`

6. **Test the tool**
   ```bash
   streamlit run app.py
   ```

   Browser should open automatically! 🎉

---

## 🐛 Troubleshooting

### Problem: "streamlit: command not found"

**Solution 1:** Use Python module syntax
```bash
python3 -m streamlit run app.py
```

**Solution 2:** Add to PATH manually
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

**Solution 3:** Use the HTML interface instead
```bash
python3 server.py
# Open http://localhost:5000
```

---

### Problem: "pip3: command not found"

**Solution:** Try `pip` instead of `pip3`
```bash
pip install -r requirements.txt
```

---

### Problem: "Permission denied"

**Solution:** Install with --user flag
```bash
pip3 install --user -r requirements.txt
```

---

### Problem: "No module named 'streamlit'"

**Solution:** Install streamlit directly
```bash
pip3 install --user streamlit
```

---

### Problem: Python version too old

**Check your Python version:**
```bash
python3 --version
```

**Should be 3.8 or higher.** If not:

**Install newer Python from:**
https://www.python.org/downloads/

---

## 🎯 Recommended Approach

**If you're new to command line:**

1. **Use the HTML Interface** - It's the easiest!
   ```bash
   cd /Users/alejandradashe/copyright-checker
   python3 server.py
   ```
   Open browser to: http://localhost:5000

2. **Use Command-Line for quick checks**
   ```bash
   python3 check.py myfile.jpg
   ```

3. **Skip Streamlit** unless you need batch processing

---

## 📦 What Each Interface Needs

| Interface | Requirements | Installation |
|-----------|--------------|--------------|
| **Command-Line** | Python 3.8+ | `pip3 install -r requirements.txt` |
| **HTML (Flask)** | Python 3.8+, Flask | `pip3 install -r requirements.txt` |
| **Streamlit** | Python 3.8+, Streamlit, PATH fix | See above |

---

## 🚀 Quick Commands Reference

### Once Installed

**Start Command-Line:**
```bash
python3 check.py <filename>
```

**Start HTML Interface:**
```bash
python3 server.py
```

**Start Streamlit (Method 1):**
```bash
streamlit run app.py
```

**Start Streamlit (Method 2 - if PATH not fixed):**
```bash
python3 -m streamlit run app.py
```

---

## ✨ Pro Tips

### Create Aliases for Easy Access

Add these to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Copyright checker aliases
alias copyright-check='python3 ~/copyright-checker/check.py'
alias copyright-web='python3 ~/copyright-checker/server.py'
alias copyright-app='python3 -m streamlit run ~/copyright-checker/app.py'
```

Then reload:
```bash
source ~/.zshrc
```

Now use from anywhere:
```bash
copyright-check myimage.jpg
copyright-web
copyright-app
```

---

## 📞 Still Having Issues?

### Check Installation Status

Run this diagnostic script:

```bash
cd /Users/alejandradashe/copyright-checker
python3 -c "
import sys
print(f'Python: {sys.version}')
try:
    import streamlit
    print(f'Streamlit: {streamlit.__version__} ✓')
except:
    print('Streamlit: NOT INSTALLED ✗')
try:
    import flask
    print(f'Flask: {flask.__version__} ✓')
except:
    print('Flask: NOT INSTALLED ✗')
try:
    import PIL
    print(f'Pillow: {PIL.__version__} ✓')
except:
    print('Pillow: NOT INSTALLED ✗')
"
```

This will show you what's installed and what's missing.

---

## 🎉 Success Checklist

After installation, you should be able to:

- [ ] Run `python3 check.py --help` (shows help)
- [ ] Run `python3 server.py` (starts web server)
- [ ] Run `streamlit run app.py` OR `python3 -m streamlit run app.py` (opens browser)
- [ ] Check a test file successfully

---

## 📚 Next Steps

Once installed:

1. Read [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed examples
2. Try checking a test file
3. Review [QUICKSTART.md](QUICKSTART.md) for usage tips

**Happy copyright checking!** 📚✓
