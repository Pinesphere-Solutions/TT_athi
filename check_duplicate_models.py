#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster

print("=" * 80)
print("CHECKING FOR DUPLICATE ModelMaster RECORDS")
print("=" * 80)

# Check for all model numbers starting with 2617
models_2617 = ModelMaster.objects.filter(model_no__startswith='2617')
print(f"\n2617 Models: {models_2617.count()}")
for m in models_2617:
    print(f"  • {m.model_no} (plating_stk_no: {m.plating_stk_no}) - {m.images.count()} images")

# Check for all model numbers starting with 1805
models_1805 = ModelMaster.objects.filter(model_no__startswith='1805')
print(f"\n1805 Models: {models_1805.count()}")
for m in models_1805:
    print(f"  • {m.model_no} (plating_stk_no: {m.plating_stk_no}) - {m.images.count()} images")
    # Show which images are missing files
    import os
    from django.conf import settings
    missing_count = 0
    for img in m.images.all():
        file_path = os.path.join(settings.MEDIA_ROOT, str(img.master_image))
        if not os.path.exists(file_path):
            missing_count += 1
    if missing_count > 0:
        print(f"     ⚠️  {missing_count} missing files")
