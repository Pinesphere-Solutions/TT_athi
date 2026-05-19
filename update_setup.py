#!/usr/bin/env python
"""Script to update module-group mapping"""

path = r'c:\Users\athit\TTT-Dev\adminportal\management\commands\setup_modules_and_groups.py'

content = '''"""
Management command: setup_modules_and_groups
============================================
Creates the five fixed User Category groups (if they don't exist) and
links each group to the Module records whose menu_title or name matches the
category's mapped value.

Run once (and re-run whenever new modules are added):
    python manage.py setup_modules_and_groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from adminportal.models import Module

# ---------------------------------------------------------------------------
# Mapping: group name  →  list of Module names or menu_titles to link
# For DP User: all three Day Planning modules (Data Upload, DP Pick Table, DP Complete Table)
# ---------------------------------------------------------------------------
CATEGORY_MENU_MAP = {
    "DP User":  ["Data Upload", "DP Pick Table", "DP Complete Table"],
    "IS User":  ["Input Screening"],
    "BQC User": ["Brass QC"],
    "IQF User": ["IQF"],
    "BA User":  ["Brass Audit"],
}


class Command(BaseCommand):
    help = (
        "Create the 5 fixed User Category groups and link them to their "
        "respective modules via the Module.groups ManyToMany field."
    )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING("Setting up User Category groups …\\n"))

        for group_name, module_names in CATEGORY_MENU_MAP.items():
            group, created = Group.objects.get_or_create(name=group_name)
            action = "Created  " if created else "Exists   "

            # Try to match by name first, then by menu_title
            modules = Module.objects.filter(name__in=module_names) | Module.objects.filter(menu_title__in=module_names)
            group.modules.set(modules)          # replace any previous links

            matched_module_names = [m.name for m in modules] or ["(no modules found — check module names/menu_titles)"]
            self.stdout.write(
                f"  {action} '{group_name}'  →  {matched_module_names}"
            )

        self.stdout.write(self.style.SUCCESS("\\nDone. Re-run this command any time new modules are added."))
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ setup_modules_and_groups.py updated successfully!")
