#!/usr/bin/env python
import os, sys, django
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print('\\n' + '='*70)
    print('  🚀 DATABASE INIT & VALIDATION FOR RENDER')
    print('='*70)
    
    # 1. Check connection
    print('\\n📋 1. Database Connection')
    print('-'*70)
    try:
        with connection.cursor() as c:
            c.execute('SELECT 1')
        print('✅ Database connection successful')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
        return 1
    
    # 2. Run migrations
    print('\\n📋 2. Running Migrations')
    print('-'*70)
    try:
        call_command('migrate', verbosity=1)
        print('✅ Migrations applied')
    except Exception as e:
        print(f'❌ Migrations failed: {e}')
        return 1
    
    # 3. Check models
    print('\\n📋 3. Model Validation')
    print('-'*70)
    try:
        django.setup()
        from mbamain.models import AUser, Project
        print('✅ Models loaded successfully')
    except Exception as e:
        print(f'❌ Model error: {e}')
        return 1
    
    print('\\n' + '='*70)
    print('  ✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT')
    print('='*70 + '\\n')
    return 0

if __name__ == '__main__':
    sys.exit(main())
