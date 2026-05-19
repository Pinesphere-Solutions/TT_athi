#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster, ModelImage

# Check detailed image paths for all three model types
for prefix in ['2617', '2648', '1805']:
    mm = ModelMaster.objects.filter(plating_stk_no__startswith=prefix).first()
    if mm:
        print(f"✅ {prefix} - {mm.plating_stk_no}")
        for img in mm.images.all():
            print(f"   Path: {img.master_image.name}")
            print(f"   URL: {img.master_image.url}")
        print()
