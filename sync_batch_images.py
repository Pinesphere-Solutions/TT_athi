#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation

print("\n" + "="*100)
print("SYNCING BATCH IMAGES WITH PARENT MODEL IMAGES")
print("="*100 + "\n")

# Get all batches
all_batches = ModelMasterCreation.objects.all()

updated_count = 0
for batch in all_batches:
    if batch.model_stock_no:
        parent_images = batch.model_stock_no.images.all()
        batch_images = batch.images.all()
        
        # Check if batch needs updating
        if batch_images.count() != parent_images.count():
            old_count = batch_images.count()
            batch.images.set(parent_images)
            updated_count += 1
            
            print(f"Updated: {batch.batch_id:40} | {batch.model_stock_no.model_no:6} | "
                  f"Old: {old_count:2} images → New: {parent_images.count():2} images")

print("\n" + "="*100)
print(f"✅ DONE! Updated {updated_count} batches")
print("="*100 + "\n")

# Verify results
print("VERIFICATION:")
print("-" * 100)
for model_no in ['2648', '2617', '1805']:
    batch = ModelMasterCreation.objects.filter(model_stock_no__model_no=model_no).first()
    if batch:
        img_count = batch.images.count()
        img_ids = list(batch.images.values_list('id', flat=True))
        print(f"{model_no}: {img_count} images - IDs: {sorted(img_ids)}")
