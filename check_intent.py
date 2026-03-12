#!/usr/bin/env python
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mbamain.models import Project
projects_with_intent = Project.objects.filter(intent_form_submitted=True).count()
print(projects_with_intent)
