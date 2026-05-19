#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation
from django.templatetags.static import static
from django.utils.safestring import mark_safe
import json

print("\n" + "="*100)
print("SIMULATING VIEW IMAGE MAPPING FOR FIRST BATCH OF EACH MODEL")
print("="*100 + "\n")

models = ['2648', '2617', '1805']

for model_no in models:
    print(f"\n{'='*100}")
    print(f"MODEL: {model_no}")
    print(f"{'='*100}")
    
    batch = ModelMasterCreation.objects.filter(model_stock_no__model_no=model_no).first()
    
    if not batch:
        print(f"❌ No batch found")
        continue
    
    print(f"Batch: {batch.batch_id}")
    print(f"Model Stock No: {batch.model_stock_no.model_no if batch.model_stock_no else 'NONE'}")
    
    # Check batch images
    batch_images = batch.images.all()
    print(f"\n1️⃣ Batch direct images: {batch_images.count()}")
    if batch_images.count() > 0:
        img_ids = list(batch_images.values_list('id', flat=True))
        print(f"   IDs: {sorted(img_ids)}")
    
    # Check model images
    model_images = batch.model_stock_no.images.all() if batch.model_stock_no else []
    print(f"2️⃣ Parent model images: {model_images.count()}")
    if model_images.count() > 0:
        img_ids = list(model_images.values_list('id', flat=True))
        print(f"   IDs: {sorted(img_ids)}")
    
    # Simulate the view logic
    images = []
    for img in batch_images:
        if hasattr(img, 'master_image') and img.master_image:
            images.append(img.master_image.url)
    
    print(f"\n📸 After checking batch.images.all(): {len(images)} images")
    
    if not images and batch.model_stock_no:
        for img in batch.model_stock_no.images.all():
            if hasattr(img, 'master_image') and img.master_image:
                images.append(img.master_image.url)
    
    print(f"📸 After fallback to model_stock_no.images: {len(images)} images")
    
    if not images:
        images = [static('assets/images/imagePlaceholder.jpg')]
        print(f"📸 Using placeholder: {images}")
    else:
        print(f"   Image URLs: {images[:3]}{'...' if len(images) > 3 else ''}")
    
    json_output = mark_safe(json.dumps(images))
    print(f"\n✅ JSON Output for template: {json_output[:100]}...")
