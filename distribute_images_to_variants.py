#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster

print("\n" + "="*100)
print("DISTRIBUTING IMAGES TO ALL MODEL VARIANTS")
print("="*100 + "\n")

# Find the master variant for each model (the one with images)
model_groups = ['2648', '2617', '1805']

for model_no in model_groups:
    masters = ModelMaster.objects.filter(model_no=model_no)
    
    # Find which variant has images
    master_with_images = None
    for m in masters:
        if m.images.count() > 0:
            master_with_images = m
            break
    
    if not master_with_images:
        print(f"\n❌ {model_no}: NO VARIANT HAS IMAGES!")
        continue
    
    print(f"\n{model_no}: Found {master_with_images.images.count()} images on {master_with_images}")
    print(f"{'='*100}")
    
    # Copy images to all other variants
    images = master_with_images.images.all()
    updated_count = 0
    
    for variant in masters:
        if variant.id != master_with_images.id:
            current_count = variant.images.count()
            variant.images.set(images)
            if current_count == 0:
                updated_count += 1
                print(f"  ✅ {variant}")
            else:
                print(f"  ⚠️  {variant} (already had {current_count} images)")
    
    print(f"\n  Updated {updated_count} variants")

print("\n" + "="*100)
print("VERIFICATION")
print("="*100 + "\n")

for model_no in model_groups:
    masters = ModelMaster.objects.filter(model_no=model_no)
    total_variants = masters.count()
    variants_with_images = sum(1 for m in masters if m.images.count() > 0)
    
    if variants_with_images == total_variants:
        print(f"✅ {model_no}: ALL {total_variants} variants have images")
    else:
        print(f"❌ {model_no}: {variants_with_images}/{total_variants} variants have images")
