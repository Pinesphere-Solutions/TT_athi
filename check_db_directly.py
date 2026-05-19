#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watchcase_tracker.settings')
django.setup()

from modelmasterapp.models import ModelMaster, ModelImage

print("\nModelMaster images for 2648:")
master = ModelMaster.objects.get(model_no='2648')
print(f"  ModelMaster ID: {master.id}")
print(f"  Direct query to through table:")

from django.db import connection
cursor = connection.cursor()
cursor.execute("""
    SELECT COUNT(*) FROM modelmasterapp_modelmaster_images 
    WHERE modelmaster_id = %s
""", [master.id])
count = cursor.fetchone()[0]
print(f"    Through table count: {count}")

cursor.execute("""
    SELECT modelimage_id FROM modelmasterapp_modelmaster_images 
    WHERE modelmaster_id = %s
    ORDER BY modelimage_id
""", [master.id])
ids = [row[0] for row in cursor.fetchall()]
print(f"    Image IDs: {ids}")
