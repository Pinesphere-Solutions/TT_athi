#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster, ModelImage

# Check all three model types
for prefix in ['2617', '2648', '1805']:
    mm = ModelMaster.objects.filter(plating_stk_no__startswith=prefix).first()
    if mm:
        img_count = mm.images.count()
        print(f"✅ {prefix} - plating_stk_no: {mm.plating_stk_no}")
        print(f"   📸 Total images linked: {img_count}")
        if img_count > 0:
            for img in mm.images.all()[:3]:
                print(f"      - {img.master_image.name}")
    else:
        print(f"❌ No ModelMaster found for {prefix}")
    print()
