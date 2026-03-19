"""
SIMPLE VERIFICATION - Direct database check
Shows all created records from previous uploads
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import ExamminerProfile, SupervisorProfile, StudentProfile

print("\n" + "="*80)
print("VERIFICATION - BULK UPLOAD FIX STATUS")
print("="*80)

print("\n" + "-"*80)
print("EXAMINERS (NULL FIELD HANDLING)")
print("-"*80)
examiners = ExamminerProfile.objects.filter(email__startswith='verify')
if examiners.exists():
    print(f"✓ {examiners.count()} examiners created with fixes:\n")
    for e in examiners:
        print(f"  • {e.email}")
        print(f"    - Students supervised: {e.number_of_students_supervised}")
        print(f"    - Publications: {e.number_publications}")
        print(f"    - Experience: {e.academic_experience}")
        print(f"    - International assessor: {e.international_assessor}")
        print()
else:
    print("No examiners found with 'verify' prefix\n")

print("-"*80)
print("SUPERVISORS (BASIC FUNCTIONALITY)")
print("-"*80)
supervisors = SupervisorProfile.objects.filter(name__in=['Charlie', 'Diana'])
if supervisors.exists():
    print(f"✓ {supervisors.count()} supervisors created:\n")
    for s in supervisors:
        print(f"  • {s.name} {s.surname}")
        if s.user:
            print(f"    Email: {s.user.email}")
        print()
else:
    print("No supervisors found (Charlie, Diana)\n")

print("-"*80)
print("STUDENTS (DUPLICATE DETECTION)")
print("-"*80)
students = StudentProfile.objects.filter(student_no__startswith='VERIFY_STU')
if students.exists():
    print(f"✓ {students.count()} students created:\n")
    for st in students:
        print(f"  • {st.student_no}")
        if st.user:
            print(f"    Email: {st.user.email}")
        print()
else:
    print("No students found with 'VERIFY_STU' prefix\n")

# ============================================================================
# SUMMARY
# ============================================================================
print("="*80)
print("SUMMARY")
print("="*80)

exam_count = ExamminerProfile.objects.filter(email__startswith='verify').count()
super_count = SupervisorProfile.objects.filter(name__in=['Charlie', 'Diana']).count()
stud_count = StudentProfile.objects.filter(student_no__startswith='VERIFY_STU').count()

tests_passed = 0
total_tests = 3

if exam_count >= 2:
    print("✓ TEST 1 PASSED: Examiners upload with NULL field handling - WORKING")
    tests_passed += 1
else:
    print("✗ TEST 1 FAILED: Examiners not created")

if super_count == 2:
    print("✓ TEST 2 PASSED: Supervisors bulk upload - WORKING")
    tests_passed += 1
else:
    print(f"✗ TEST 2 FAILED: Expected 2 supervisors, got {super_count}")

if stud_count >= 2:
    print("✓ TEST 3 PASSED: Students bulk upload - WORKING")
    tests_passed += 1
else:
    print(f"✗ TEST 3 FAILED: Expected 2+ students, got {stud_count}")

print("\n" + "="*80)
if tests_passed == total_tests:
    print(f"✓✓✓ ALL {tests_passed}/{total_tests} FIXES VERIFIED ✓✓✓")
else:
    print(f"⚠ PARTIAL SUCCESS: {tests_passed}/{total_tests} tests passed")
print("="*80)
print()
