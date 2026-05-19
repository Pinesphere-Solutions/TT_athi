#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelImage

print("\n" + "="*100)
print("CHECKING ACTUAL IMAGE URLs IN DATABASE")
print("="*100 + "\n")

# Group by model
image_groups = {
    '2648': (1, 16),
    '2617': (17, 32),
    '1805': (33, 40)
}

for model_no, (start, end) in image_groups.items():
    print(f"\n{model_no} Images (IDs {start}-{end}):")
    print("-" * 100)
    
    for img_id in range(start, end + 1):
        try:
            img = ModelImage.objects.get(id=img_id)
            url = img.master_image.url if img.master_image else "NO FILE"
            file_path = img.master_image.name if img.master_image else "N/A"
            file_check_path = f'media/{file_path}'
            exists = "✅" if os.path.exists(file_check_path) else "❌"
            print(f"  ID {img_id}: {exists} {url}")
        except ModelImage.DoesNotExist:
            print(f"  ID {img_id}: NOT IN DATABASE ❌")

print("\n" + "="*100)
