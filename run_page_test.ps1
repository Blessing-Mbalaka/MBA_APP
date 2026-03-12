# MBA Application - Page Loading Test Suite
# PowerShell script to run the page loading test with proper Django environment

$projectPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Path
Set-Location $projectPath

Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "  MBA Application - Page Loading Test Suite" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Django is available
Write-Host "Checking Django installation..." -ForegroundColor Yellow
$djangoCheck = python -c "import django; print('OK')" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: Django might not be installed in the current environment" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To properly run this test:" -ForegroundColor Yellow
    Write-Host "1. Ensure your Python environment with Django is activated" -ForegroundColor Yellow
    Write-Host "2. Run: python -m pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "3. Then run this script again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or run the test directly with:" -ForegroundColor Yellow
    Write-Host "   python manage.py test_page_loading" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue anyway (may fail)"
}

Write-Host "Running page loading tests..." -ForegroundColor Green
Write-Host ""

# Run the test
python manage.py test_page_loading
$testExitCode = $LASTEXITCODE

Write-Host ""

if ($testExitCode -eq 0) {
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "  ✓ ALL TESTS PASSED" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
} else {
    Write-Host "================================================================================" -ForegroundColor Red
    Write-Host "  ✗ SOME TESTS FAILED" -ForegroundColor Red
    Write-Host "================================================================================" -ForegroundColor Red
}

Write-Host ""
Write-Host "Check 'logs.txt' for detailed results" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
exit $testExitCode
