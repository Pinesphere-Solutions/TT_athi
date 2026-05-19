#!/usr/bin/env python
"""Check all modules in the database"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from adminportal.models import Module

print("All modules in database:")
print("-" * 60)
modules = Module.objects.all().order_by('name')
for m in modules:
    print(f"  ID: {m.id:2d} | Name: {m.name:30s} | Menu: {m.menu_title or 'N/A'}")

print(f"\nTotal: {modules.count()} modules")

# Search for "Data Upload" or "DP Completed" or "DP Complete"
print("\n" + "="*60)
print("Searching for Day Planning related modules...")
dp_related = Module.objects.filter(name__icontains='Data')
print(f"Modules containing 'Data': {dp_related.count()}")
for m in dp_related:
    print(f"  - {m.name}")

dp_related = Module.objects.filter(name__icontains='Completed')
print(f"Modules containing 'Completed': {dp_related.count()}")
for m in dp_related:
    print(f"  - {m.name}")

dp_related = Module.objects.filter(name__icontains='Complete')
print(f"Modules containing 'Complete': {dp_related.count()}")
for m in dp_related:
    print(f"  - {m.name}")

dp_related = Module.objects.filter(name__icontains='DP')
print(f"Modules containing 'DP': {dp_related.count()}")
for m in dp_related:
    print(f"  - {m.name}")
