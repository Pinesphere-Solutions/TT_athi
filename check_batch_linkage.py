#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation

print("=" * 80)
print("CHECKING 2617 BATCH -> MODELMASTER LINKAGE")
print("=" * 80)

# Get batches for 2617
batches = ModelMasterCreation.objects.filter(
    model_stock_no__model_no='2617'
).prefetch_related('model_stock_no__images')[:3]

for batch in batches:
    print(f"\n📦 Batch: {batch.batch_id}")
    print(f"   model_stock_no: {batch.model_stock_no}")
    print(f"   model_stock_no.plating_stk_no: {batch.model_stock_no.plating_stk_no}")
    print(f"   model_stock_no.images.count(): {batch.model_stock_no.images.count()}")
    
    # Show first 2 images
    for i, img in enumerate(batch.model_stock_no.images.all()[:2], 1):
        print(f"   - Image {i}: {img.master_image.url}")

print("\n" + "=" * 80)
print("CHECKING 1805 BATCH -> MODELMASTER LINKAGE")
print("=" * 80)

# Get batches for 1805
batches = ModelMasterCreation.objects.filter(
    model_stock_no__model_no='1805'
).prefetch_related('model_stock_no__images')[:3]

for batch in batches:
    print(f"\n📦 Batch: {batch.batch_id}")
    print(f"   model_stock_no: {batch.model_stock_no}")
    print(f"   model_stock_no.plating_stk_no: {batch.model_stock_no.plating_stk_no}")
    print(f"   model_stock_no.images.count(): {batch.model_stock_no.images.count()}")
    
    # Show all images
    for i, img in enumerate(batch.model_stock_no.images.all(), 1):
        print(f"   - Image {i}: {img.master_image.url}")
