#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelImage, ModelMaster, ModelMasterCreation

print("\n" + "="*100)
print("VERIFYING IMAGE LINKAGE FOR EACH MODEL")
print("="*100 + "\n")

# Get sample batches from each model
models_to_test = ['2648', '2617', '1805']

for model_no in models_to_test:
    print(f"\n{'='*100}")
    print(f"MODEL: {model_no}")
    print(f"{'='*100}")
    
    # Find ModelMaster for this model
    master = ModelMaster.objects.filter(model_no=model_no).first()
    if not master:
        print(f"❌ No ModelMaster found for {model_no}")
        continue
    
    print(f"\nModelMaster: {master.model_no}")
    print(f"  Direct images linked: {master.images.count()}")
    if master.images.count() > 0:
        image_ids = list(master.images.values_list('id', flat=True))
        print(f"  Image IDs: {sorted(image_ids)}")
    
    # Find ModelMasterCreation batches
    batches = ModelMasterCreation.objects.filter(model_stock_no=master).first()
    if batches:
        print(f"\nSample Batch: {batches.batch_id}")
        print(f"  Direct images: {batches.images.count()}")
        if batches.images.count() > 0:
            image_ids = list(batches.images.values_list('id', flat=True))
            print(f"  Image IDs: {sorted(image_ids)}")
        
        print(f"  Parent model images: {batches.model_stock_no.images.count()}")
        if batches.model_stock_no.images.count() > 0:
            image_ids = list(batches.model_stock_no.images.values_list('id', flat=True))
            print(f"  Image IDs: {sorted(image_ids)}")
    else:
        print(f"\n❌ No batches found for {model_no}")

print("\n" + "="*100)
print("IMAGE OWNERSHIP")
print("="*100)

# Check which models own which images
for img_id in range(1, 41):
    try:
        img = ModelImage.objects.get(id=img_id)
        owners = img.modelmaster_set.all()
        owner_list = [f"{m.model_no}" for m in owners]
        if owner_list:
            print(f"Image {img_id}: Owned by {', '.join(owner_list)}")
        else:
            print(f"Image {img_id}: ❌ NO OWNER")
    except ModelImage.DoesNotExist:
        print(f"Image {img_id}: NOT IN DATABASE")
