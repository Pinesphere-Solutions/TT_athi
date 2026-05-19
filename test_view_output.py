#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMasterCreation
from django.templatetags.static import static
from django.utils.safestring import mark_safe

print("\n" + "="*100)
print("SIMULATING VIEW OUTPUT FOR EACH MODEL (FIRST BATCH)")
print("="*100 + "\n")

models = ['2648', '2617', '1805']

for model_no in models:
    batch = ModelMasterCreation.objects.filter(model_stock_no__model_no=model_no).first()
    
    if not batch:
        print(f"❌ No batch for {model_no}")
        continue
    
    print(f"\n{model_no} - {batch.batch_id}")
    print("-" * 100)
    
    # Simulate view logic
    mmc = ModelMasterCreation.objects.filter(batch_id=batch.batch_id).first()
    images = []
    if mmc:
        for img in getattr(mmc, 'images', []).all():
            if getattr(img, 'master_image', None):
                images.append(img.master_image.url)
    
    if not images:
        images = [static('assets/images/imagePlaceholder.jpg')]
    
    print(f"Raw images list: {images}")
    
    # JSON serialize
    json_output = mark_safe(json.dumps(images))
    print(f"JSON output: {json_output}")
    print(f"JSON output (type): {type(json_output)}")
    
    # Check what would appear in template
    print(f"In template: data-model-images='{json_output}'")
