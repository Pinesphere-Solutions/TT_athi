#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster

print("\nAll ModelMaster records:\n")

for model_no in ['2648', '2617', '1805']:
    masters = ModelMaster.objects.filter(model_no=model_no)
    print(f"\n{model_no}: {masters.count()} variants")
    for m in masters:
        images = m.images.all()
        img_ids = list(images.values_list('id', flat=True))
        print(f"  ID {m.id:3}: {str(m):40} | {len(img_ids):2} images: {img_ids[:5]}")
