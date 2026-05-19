#!/usr/bin/env python
"""Script to directly update module-group mappings in the database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from django.contrib.auth.models import Group
from adminportal.models import Module

# Module names to assign to each group
CATEGORY_MENU_MAP = {
    "DP User":  ["Data Upload", "DP Pick Table", "DP Complete Table"],
    "IS User":  ["Input Screening"],
    "BQC User": ["Brass QC"],
    "IQF User": ["IQF"],
    "BA User":  ["Brass Audit"],
}

print("[ModuleAssignment] Setting up User Category groups...")
for group_name, module_names in CATEGORY_MENU_MAP.items():
    group, created = Group.objects.get_or_create(name=group_name)
    action = "Created" if created else "Updated"

    # Try to match by name first, then by menu_title
    modules = Module.objects.filter(name__in=module_names) | Module.objects.filter(menu_title__in=module_names)
    group.modules.set(modules)

    matched_module_names = [m.name for m in modules] or ["(no modules found)"]
    print(f"  [{action}] '{group_name}' → {matched_module_names}")

print("[ModuleAssignment] ✓ Done!")
