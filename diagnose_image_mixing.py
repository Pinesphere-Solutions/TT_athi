#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation, ModelImage

print("=" * 100)
print("DIAGNOSING IMAGE MIXING ISSUE")
print("=" * 100)

# Get image ID ranges
print("\n📊 IMAGE ID RANGES:")
print("-" * 100)
images = ModelImage.objects.all().order_by('id')
for img in images:
    print(f"ID {img.id}: {img.master_image} -> linked to: {img.modelmaster_set.first() or img.modelstockno_set.first()}")

print("\n\n" + "=" * 100)
print("CHECKING BATCH -> MODELMASTER LINKAGE")
print("=" * 100)

# Check a batch from each model
for model_no in ['2617', '2648', '1805']:
    print(f"\n\n🔍 MODEL: {model_no}")
    print("-" * 100)
    
    batches = ModelMasterCreation.objects.filter(
        model_stock_no__model_no=model_no
    ).prefetch_related('model_stock_no__images')[:1]
    
    for batch in batches:
        print(f"Batch: {batch.batch_id}")
        print(f"  model_stock_no (FK): {batch.model_stock_no}")
        print(f"  model_stock_no.plating_stk_no: {batch.model_stock_no.plating_stk_no}")
        print(f"  model_stock_no.model_no: {batch.model_stock_no.model_no}")
        print(f"  Images count: {batch.model_stock_no.images.count()}")
        
        print(f"\n  Image IDs linked to this ModelMaster:")
        for i, img in enumerate(batch.model_stock_no.images.all(), 1):
            print(f"    Image {i}: ID={img.id}, filename={img.master_image}")
        
        # Show which model_no owns these images
        print(f"\n  Checking image ownership:")
        first_img = batch.model_stock_no.images.first()
        if first_img:
            # Find which ModelMaster owns this image
            for mm in first_img.modelmaster_set.all():
                print(f"    ⚠️  Image {first_img.id} is also linked to ModelMaster: {mm.plating_stk_no} (model_no={mm.model_no})")

print("\n\n" + "=" * 100)
print("SUMMARY: Check if images are linked to MULTIPLE ModelMasters")
print("=" * 100)
