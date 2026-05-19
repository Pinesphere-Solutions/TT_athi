#!/usr/bin/env python
"""Test script to verify DP-User gets all three Day Planning modules"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from django.contrib.auth.models import User, Group
from adminportal.models import UserProfile, Module, UserModuleProvision
from adminportal.views import assign_modules_to_user_by_group

# Test 1: Check if modules exist in database
print("[TEST 1] Checking if Day Planning modules exist...")
dp_modules = Module.objects.filter(name__in=["Data Upload", "DP Pick Table", "DP Complete Table"])
print(f"  Found {dp_modules.count()} modules:")
for m in dp_modules:
    print(f"    - {m.name} (menu_title: {m.menu_title})")

# Test 2: Create or get DP User group
print("\n[TEST 2] Setting up DP User group...")
dp_group, created = Group.objects.get_or_create(name="DP User")
print(f"  Group 'DP User': {'CREATED' if created else 'EXISTS'}")

# Test 3: Create a test user
test_username = "test_dp_user_123"
print(f"\n[TEST 3] Creating test user '{test_username}'...")
test_user, user_created = User.objects.get_or_create(
    username=test_username,
    defaults={'email': f'{test_username}@test.com'}
)
if user_created:
    print(f"  User CREATED")
else:
    print(f"  User EXISTS (will reassign modules)")

# Test 4: Assign modules using the function
print("\n[TEST 4] Assigning modules to test user...")
assign_modules_to_user_by_group(test_user, dp_group)

# Test 5: Verify module assignments
print("\n[TEST 5] Verifying module assignments...")
assigned_modules = UserModuleProvision.objects.filter(user=test_user)
print(f"  User {test_username} has {assigned_modules.count()} module(s):")
for prov in assigned_modules:
    print(f"    - {prov.module_name}")

# Check if all 3 required modules are present
required_modules = {"Data Upload", "DP Pick Table", "DP Complete Table"}
assigned_names = set(assigned_modules.values_list('module_name', flat=True))
missing = required_modules - assigned_names

if not missing:
    print(f"\n  ✓ SUCCESS: All required modules assigned!")
else:
    print(f"\n  ✗ FAILED: Missing modules: {missing}")

# Test 6: Cleanup
print("\n[TEST 6] Cleaning up test user...")
assigned_modules.delete()
test_user.delete()
print("  Test user and assignments deleted")

print("\n" + "="*60)
print("SUMMARY:")
print("  If all 3 modules (Data Upload, DP Pick Table, DP Complete")
print("  Table) appear above, the fix is working correctly!")
print("="*60)
