#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster, ModelImage

# Fix image paths for 2648 and 1805 - remove 'model_images/' prefix
fixed_count = 0

for prefix in ['2648', '1805']:
    mm = ModelMaster.objects.filter(plating_stk_no__startswith=prefix).first()
    if mm:
        for img in mm.images.all():
            if 'model_images/' in img.master_image.name:
                old_path = img.master_image.name
                new_path = img.master_image.name.replace('model_images/', '')
                img.master_image.name = new_path
                img.save()
                fixed_count += 1
                print(f"✅ Fixed: {old_path} → {new_path}")

print(f"\n📊 Total fixed: {fixed_count} image paths")
