# PAGE LOADING TEST - QUICK START GUIDE

## 📋 Overview
This test automatically checks all pages in your MBA application to ensure they load properly without returning 404 errors. Results are saved to `logs.txt` and displayed in the terminal with color-coded output.

---

## 🚀 FASTEST WAY TO RUN (Choose One)

### **Option 1: Using the Management Command (RECOMMENDED)**
```bash
python manage.py test_page_loading
```
- Simplest command
- Works after Django is properly installed
- Best for CI/CD integration

### **Option 2: PowerShell Script (Windows)**
Double-click or run in PowerShell:
```powershell
.\run_page_test.ps1
```
- Handles environment checking
- Shows helpful error messages
- Interactive with pause

### **Option 3: Batch File (Windows)**
Double-click:
```
run_page_test.bat
```
- Simple Windows batch file
- No PowerShell knowledge needed

### **Option 4: Python Script (Cross-Platform)**
```bash
python test_pages.py
```
- Works on Windows, Mac, Linux
- Standalone execution
- Good for automation

### **Option 5: Setup & Test (Auto-Install Dependencies)**
```bash
python setup_and_test.py
```
- Automatically installs dependencies
- Then runs the test
- Best if pip is working

---

## ⚙️ SETUP REQUIRED (Only Once)

Before running any test, ensure:

1. **Navigate to project directory:**
   ```bash
   cd "c:\Users\bjmba\OneDrive\Desktop\Deployed MBA App\mba_application"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   OR if Django is already working (you can run `python manage.py runserver`):
   - Just run any of the commands above!

---

## 📊 WHAT YOU'LL SEE

### Terminal Output Example:
```
================================================================================
  PAGE LOADING TEST SUITE
================================================================================

Found 86 URL patterns

Testing URLs...

✓ PASS | /                                                 | index                         | 302
✓ PASS | /signin                                           | signin                        | 200
✓ PASS | /admin/                                           | index                         | 200
✗ FAIL | /nonexistent-page                                 | unknown                       | 404

================================================================================
  TEST SUMMARY
================================================================================

✓ Passed: 84 | ✗ Failed: 2 | Total: 86

FAILED PAGES:

  • /nonexistent-page (unknown) - Page not found (404)

Log file saved to: c:\Users\bjmba\OneDrive\Desktop\Deployed MBA App\mba_application\logs.txt
```

### Logs File (`logs.txt`)
- Complete summary with counts
- Detailed list of failed pages with reasons
- List of all passed pages
- Timestamp of test run

---

## 📁 FILES INCLUDED

| File | Purpose |
|------|---------|
| `test_pages.py` | Standalone Python test script |
| `mbaAdmin/management/commands/test_page_loading.py` | Django management command |
| `run_page_test.bat` | Windows batch launcher |
| `run_page_test.ps1` | Windows PowerShell launcher |
| `setup_and_test.py` | Auto-install dependencies + test |
| `PAGE_LOADING_TEST_README.md` | Detailed documentation |
| `logs.txt` | Test results (generated after running) |

---

## ❌ TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'django'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "No module named 'django.core.management'"
**Solution:** You're using the wrong Python environment. Make sure you're using the Python that has Django installed:
```bash
# Check if Django is installed
python -c "import django; print('OK')"

# If not, install it
pip install django
```

### Test runs but shows "SERVER ERROR (500)" or similar
This might indicate actual bugs in your pages. Check the `logs.txt` file for details and check your Django console for error messages.

### "Permission denied" or similar errors on Windows
Try running from an Administrator prompt:
1. Open PowerShell or Command Prompt as Administrator
2. Navigate to your project
3. Run the test

---

## 🔧 INTEGRATION TIPS

### Run tests automatically during development
```bash
# After making changes
python manage.py test_page_loading
```

### Add to your build/CI pipeline
```bash
# In GitHub Actions, GitLab CI, etc.
python manage.py test_page_loading || exit 1
```

### Check for specific pages
The test logs to `logs.txt` - open it to see exactly which pages failed and why.

---

## ✅ SUCCESS INDICATORS

- ✓ All URLs tested without errors
- ✓ Pretty colored terminal output (green = pass, red = fail)
- ✓ `logs.txt` file created with summary
- ✓ No 404 errors (unless expected)
- ✓ Quick execution (usually < 1 minute)

---

## 📝 NOTES

- **Parameterized URLs**: URLs with parameters (like `/projects/1`, `/admin/15`) are tested with the number `1` as the default parameter
- **Methods tested**: GET requests only
- **Redirects**: Followed automatically (301, 302 redirects are counted as success)
- **Server must be off**: Run test when Django server is not running (to avoid conflicts)

---

## 🆘 STILL HAVING ISSUES?

1. Make sure Django server is **NOT** running
2. Check that you're in the right directory (where `manage.py` is)
3. Verify requirements are installed: `pip list | grep -i django`
4. Check `logs.txt` for error details
5. Look at Django's settings.py for configuration issues

---

**Version:** 1.0  
**Created:** March 8, 2026  
**Updated:** March 8, 2026
