#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation

print("\n" + "="*100)
print("CHECKING PAGE ORDER - What model batches appear first?")
print("="*100 + "\n")

batches = ModelMasterCreation.objects.filter(
    total_batch_quantity__gt=0,
    Moved_to_D_Picker=False
).order_by('-date_time', 'batch_id')[:50]

print(f"Total batches matching filter: {batches.count()}")
print(f"\nFirst 20 batches:\n")

for i, batch in enumerate(batches[:20], 1):
    model_no = batch.model_stock_no.model_no if batch.model_stock_no else "NONE"
    img_count = batch.images.count()
    print(f"{i:2}. {batch.batch_id:40} | Model: {model_no:6} | Images: {img_count}")
