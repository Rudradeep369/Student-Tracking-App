#!/usr/bin/env python3
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
django.setup()

from myapp.forms import StudyMaterialForm

# Test data
test_data = {
    'title': 'Test Science Material',
    'description': 'Test description',
    'board': 'WBBSE',
    'class_level': 5,
    'subject': 'Science',
    'google_drive_link': 'https://drive.google.com/file/d/test',
    'is_active': True
}

print("Testing StudyMaterial form with data:", test_data)
form = StudyMaterialForm(data=test_data)

print("Form is valid:", form.is_valid())
if not form.is_valid():
    print("Form errors:", form.errors)
    print("Non-field errors:", form.non_field_errors())
else:
    print("Form would save successfully!")
    # Don't actually save during test
    # form.save()
