#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation

print("\n" + "="*100)
print("CHECKING BATCH IMAGES AFTER SYNC")
print("="*100 + "\n")

models = ['2648', '2617', '1805']

for model_no in models:
    batches = ModelMasterCreation.objects.filter(model_stock_no__model_no=model_no)
    print(f"\n{model_no}: {batches.count()} batches")
    print("-" * 100)
    
    for batch in batches[:3]:  # Show first 3 batches
        img_count = batch.images.count()
        img_ids = list(batch.images.values_list('id', flat=True))[:5]  # Show first 5 IDs
        parent_img_count = batch.model_stock_no.images.count()
        print(f"  {batch.batch_id:40} | Batch images: {img_count:2} | Parent images: {parent_img_count:2}")
        if img_count > 0:
            print(f"    → IDs: {sorted(img_ids)}")
