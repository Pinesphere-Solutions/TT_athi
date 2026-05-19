#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User

from DayPlanning.views import DPPickTableView
from modelmasterapp.models import ModelMasterCreation

print("\n" + "="*100)
print("CHECKING HTML RENDERING - What's actually being sent to template?")
print("="*100 + "\n")

factory = RequestFactory()
request = factory.get('/dp-pick-table/')

# Create a test user
user, created = User.objects.get_or_create(username='testuser', defaults={'is_staff': True})
request.user = user

view = DPPickTableView()
view.request = request

# Get context
context = view.get_context_data()

# Check the data for first few rows
rows = context.get('page_obj', [])
print(f"Total rows on first page: {len(rows)}\n")

for i, row in enumerate(rows[:5], 1):
    model_no = row.model_stock_no.model_no if row.model_stock_no else "NONE"
    # row is now a dictionary, check for model_images
    model_images = row.get('model_images') if isinstance(row, dict) else getattr(row, 'model_images', 'NOT FOUND')
    img_count = row.get('images') if isinstance(row, dict) else getattr(row, 'images', 'NOT FOUND')
    
    print(f"{i}. Batch: {row.get('batch_id')}")
    print(f"   Model: {model_no}")
    print(f"   model_images attr type: {type(model_images)}")
    print(f"   model_images value: {model_images[:100] if model_images != 'NOT FOUND' else 'NOT FOUND'}...")
    print()
