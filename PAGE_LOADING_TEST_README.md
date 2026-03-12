# Page Loading Test Suite

This test suite checks all pages in your MBA application to ensure they load properly without 404 errors.

## Quick Start

### Option 1: Run as Management Command (Recommended)

First, ensure your environment is set up with Django installed:

```bash
# Navigate to the project directory
cd "c:\Users\bjmba\OneDrive\Desktop\Deployed MBA App\mba_application"

# Make sure dependencies are installed
pip install -r requirements.txt

# Run the test
python manage.py test_page_loading
```

### Option 2: Run the Standalone Script

```bash
cd "c:\Users\bjmba\OneDrive\Desktop\Deployed MBA App\mba_application"
pip install -r requirements.txt
python test_pages.py
```

### Option 3: Use the Batch File (Windows)

Simply double-click:
```
run_page_test.bat
```

## What the Test Does

✓ **Discovers all URLs** from your Django URL patterns  
✓ **Tests each URL** to ensure it doesn't return a 404  
✓ **Logs failures** to `logs.txt` with detailed information  
✓ **Pretty prints results** to the terminal with color-coded output  
✓ **Generates statistics** showing pass/fail counts  

## Output

### Terminal Output
The test displays real-time results in the terminal:
- ✓ PASS (green) for successful pages
- ✗ FAIL (red) for failed pages
- Shows HTTP status codes
- Shows URL names and paths

### Log File
A `logs.txt` file is created with:
- Complete summary of test results
- List of all failed pages with details
- List of all passed pages
- Timestamp of when the test was run

## Example Output

```
================================================================================
  PAGE LOADING TEST SUITE
================================================================================

Found 86 URL patterns

Testing URLs...

✓ PASS | /                                                 | index                         | 200
✓ PASS | /signin                                           | signin                        | 200
✓ PASS | /admin/scholars                                   | scholars                      | 200
✗ FAIL | /unknown-page                                     | unknown                       | 404

================================================================================
  TEST SUMMARY
================================================================================

✓ Passed: 84 | ✗ Failed: 2 | Total: 86

FAILED PAGES:

  • /unknown-page (unknown) - Page not found (404)
  • /another-page (another) - Page not found (404)

Log file saved to: c:\Users\bjmba\OneDrive\Desktop\Deployed MBA App\mba_application\logs.txt
```

## Files Included

1. **test_pages.py** - Standalone Python script that can be run directly
2. **mbaAdmin/management/commands/test_page_loading.py** - Django management command
3. **run_page_test.bat** - Windows batch file for easy execution
4. **logs.txt** - Auto-generated log file with test results

## Requirements

- Django (should already be in requirements.txt)
- Colorama (for colored terminal output - already in requirements.txt)

## Troubleshooting

### "ModuleNotFoundError: No module named 'django'"

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Import errors or Django setup issues

Ensure you're running the command from the project root directory where `manage.py` is located.

### Virtual Environment Issues

If you're using a virtual environment, make sure it's activated before running the test:
```bash
# Activate virtual environment (if using one)
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

## Integration with CI/CD

You can integrate this test into your CI/CD pipeline:

```bash
python manage.py test_page_loading && echo "All pages loaded successfully!"
```

The script exits with code 0 if all tests pass, and code 1 if any fail.

---

**Created:** March 8, 2026  
**Author:** GitHub Copilot  
**Purpose:** Automated page loading audit for MBA Application
