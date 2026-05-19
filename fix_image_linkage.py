#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelImage, ModelMaster

print("=" * 100)
print("FIXING IMAGE LINKAGE - CORRECT MAPPING")
print("=" * 100)

# CORRECT image ID ranges (as user confirmed)
image_ranges = {
    '2648': (1, 16),      # Images 1-16 belong to 2648
    '2617': (17, 32),     # Images 17-32 belong to 2617
    '1805': (33, 40),     # Images 33-40 belong to 1805
}

# Create mapping of which model each image should belong to
correct_model_mapping = {}
for model_no, (start_id, end_id) in image_ranges.items():
    for img_id in range(start_id, end_id + 1):
        correct_model_mapping[img_id] = model_no

print("\n✅ CORRECT IMAGE OWNERSHIP MAPPING:")
print("-" * 100)
for img_id, model_no in sorted(correct_model_mapping.items()):
    if img_id in [1, 17, 33]:  # Show markers
        print(f"\n{model_no} images:")
    print(f"  Image ID {img_id}: Belongs to model {model_no}")

print("\n\n⚙️  FIXING ALL IMAGE LINKAGES:")
print("-" * 100)

total_removed = 0
total_added = 0

# For each image, clear ALL links and add ONLY the correct one
for img_id, correct_model_no in correct_model_mapping.items():
    img = ModelImage.objects.get(id=img_id)
    
    # Get all ModelMaster records currently linked to this image
    linked_models = list(img.modelmaster_set.all())
    
    # Get the correct ModelMaster to link to
    correct_model = ModelMaster.objects.filter(model_no=correct_model_no).first()
    
    if not correct_model:
        print(f"⚠️  WARNING: No ModelMaster found for model {correct_model_no}")
        continue
    
    # Remove ALL current links
    for mm in linked_models:
        img.modelmaster_set.remove(mm)
        total_removed += 1
    
    # Add link to correct model
    if correct_model not in img.modelmaster_set.all():
        img.modelmaster_set.add(correct_model)
        total_added += 1
    
    if img_id in [1, 17, 33, 40]:  # Show progress at key points
        print(f"Image {img_id} ({img.master_image}): Linked to {correct_model.plating_stk_no}")

print(f"\n{'=' * 100}")
print(f"✅ DONE!")
print(f"   Removed {total_removed} incorrect links")
print(f"   Added {total_added} correct links")
print(f"{'=' * 100}")

# Verify the fix
print("\n\n🔍 VERIFICATION - Final image distribution:")
print("-" * 100)

for model_no in ['2648', '2617', '1805']:
    variants = ModelMaster.objects.filter(model_no=model_no)
    
    # Get all unique images linked to ANY variant of this model
    all_img_ids = set()
    
    for variant in variants:
        img_ids = list(variant.images.all().values_list('id', flat=True))
        all_img_ids.update(img_ids)
    
    expected_start, expected_end = image_ranges[model_no]
    expected_ids = list(range(expected_start, expected_end + 1))
    
    print(f"\n{model_no}:")
    print(f"  Expected IDs: {expected_ids}")
    print(f"  Actual IDs:   {sorted(all_img_ids)}")
    
    if sorted(all_img_ids) == expected_ids:
        print(f"  ✅ CORRECT!")
    else:
        print(f"  ❌ MISMATCH!")
        missing = set(expected_ids) - all_img_ids
        extra = all_img_ids - set(expected_ids)
        if missing:
            print(f"     Missing: {sorted(missing)}")
        if extra:
            print(f"     Extra: {sorted(extra)}")


