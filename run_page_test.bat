@echo off
REM Page Loading Test Script for MBA Application
REM Run this from the project directory

cd /d "c:\Users\bjmba\OneDrive\Desktop\Deployed MBA App\mba_application"

echo.
echo ================================================================================
echo  MBA Application - Page Loading Test Suite
echo ================================================================================
echo.

REM Try to run the test using the Django management command
echo Running page loading tests...
echo.

python manage.py test_page_loading

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo  TEST COMPLETED SUCCESSFULLY
    echo ================================================================================
    echo Check logs.txt for detailed results
) else (
    echo.
    echo ================================================================================
    echo  TEST FAILED - Some pages did not load correctly
    echo ================================================================================
    echo Check logs.txt for detailed results
)

echo.
pause
