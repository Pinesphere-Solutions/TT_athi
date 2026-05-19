#!/usr/bin/env python
"""Create missing Day Planning modules in the database"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from adminportal.models import Module

print("Creating missing Day Planning modules...")
print("-" * 60)

# Modules to create
modules_to_create = [
    {"name": "Data Upload", "menu_title": "Day Planning", "headings": []},
    {"name": "DP Complete Table", "menu_title": "Day Planning", "headings": []},
]

for module_data in modules_to_create:
    module, created = Module.objects.get_or_create(
        name=module_data["name"],
        defaults={
            "menu_title": module_data["menu_title"],
            "headings": module_data["headings"]
        }
    )
    status = "CREATED" if created else "EXISTS"
    print(f"  {module.name}: {status}")

# Verify all modules now exist
print("\n" + "="*60)
print("All modules after creation:")
print("-" * 60)
modules = Module.objects.all().order_by('name')
for m in modules:
    print(f"  - {m.name}")

print(f"\nTotal modules: {modules.count()}")
