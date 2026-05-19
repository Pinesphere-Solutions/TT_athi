#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation

print("\n" + "="*100)
print("ALL BATCHES AND THEIR MODELS")
print("="*100 + "\n")

batches = ModelMasterCreation.objects.all()[:20]

for batch in batches:
    model_no = batch.model_stock_no.model_no if batch.model_stock_no else "NONE"
    print(f"Batch: {batch.batch_id:15} | Model: {model_no:10} | Total Qty: {batch.total_batch_quantity}")

print(f"\nTotal batches: {ModelMasterCreation.objects.count()}")
print(f"\nBatches by model:")
for model_no in ['2648', '2617', '1805']:
    count = ModelMasterCreation.objects.filter(model_stock_no__model_no=model_no).count()
    print(f"  {model_no}: {count} batches")
