#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster, ModelMasterCreation, ModelImage
from django.conf import settings
import json

print("=" * 80)
print("DIAGNOSING 2617 AND 1805 IMAGE ISSUES")
print("=" * 80)

# Check ModelMaster images for 2617 and 1805
for model_no in ['2617', '1805']:
    print(f"\n📋 MODEL: {model_no}")
    print("-" * 80)
    
    # Find ModelMaster
    mm = ModelMaster.objects.filter(plating_stk_no__startswith=model_no).first()
    if mm:
        print(f"✅ Found ModelMaster: {mm.plating_stk_no}")
        print(f"   Images linked to ModelMaster: {mm.images.count()}")
        
        for i, img in enumerate(mm.images.all(), 1):
            print(f"\n   Image {i}:")
            print(f"   - master_image path: {img.master_image}")
            print(f"   - master_image.url: {img.master_image.url}")
            
            # Check if file exists
            file_path = os.path.join(settings.MEDIA_ROOT, str(img.master_image))
            exists = os.path.exists(file_path)
            print(f"   - File exists: {exists}")
            if not exists:
                print(f"     ❌ Missing file: {file_path}")
    else:
        print(f"❌ No ModelMaster found for {model_no}")

# Check ModelMasterCreation for these models
print(f"\n\n📋 CHECKING ModelMasterCreation BATCHES")
print("-" * 80)

for model_no in ['2617', '1805']:
    mmc_list = ModelMasterCreation.objects.filter(
        model_stock_no__model_no=model_no
    ).prefetch_related('images', 'model_stock_no__images')[:3]
    
    if mmc_list:
        print(f"\n✅ Found {mmc_list.count()} batches for model {model_no}")
        for batch in mmc_list[:3]:
            print(f"\n   Batch: {batch.batch_id}")
            print(f"   - Batch images: {batch.images.count()}")
            print(f"   - Parent ModelMaster images: {batch.model_stock_no.images.count()}")
            
            # Show parent images
            if batch.model_stock_no:
                print(f"   - Parent model: {batch.model_stock_no.plating_stk_no}")
                for img in batch.model_stock_no.images.all():
                    print(f"     • {img.master_image.url}")
    else:
        print(f"\n❌ No batches found for model {model_no}")

# Check media directory
print(f"\n\n📁 CHECKING MEDIA DIRECTORY")
print("-" * 80)

media_root = settings.MEDIA_ROOT
print(f"MEDIA_ROOT: {media_root}")
print(f"Exists: {os.path.exists(media_root)}")

if os.path.exists(media_root):
    files = os.listdir(media_root)
    print(f"Files in /media/: {len(files)}")
    
    # Filter for 2617 and 1805 images
    for filename in files:
        if '2617' in filename or '1805' in filename or 'front' in filename.lower():
            print(f"  • {filename}")
