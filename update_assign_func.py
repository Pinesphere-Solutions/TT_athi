#!/usr/bin/env python
"""Script to update the assign_modules_to_user_by_group function"""

path = r'c:\Users\athit\TTT-Dev\adminportal\views.py'

# Read the file
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old function
old_func = '''def assign_modules_to_user_by_group(user, group):
    """
    Automatically assign modules to a user based on their user category (group).
    This ensures that:
    - Admin group: Gets access to ALL modules
    - Other groups (DP-User, BQC-User, etc.): Get ONLY the modules linked to that group
    - No group: Gets NO modules
    
    This function clears any existing UserModuleProvision records and recreates them.
    """
    from django.contrib.auth.models import Group
    
    # Clear all existing module provisions for this user
    UserModuleProvision.objects.filter(user=user).delete()
    
    if not group:
        logger.info(f"[ModuleAssignment] User {user.username} has no group assigned, no modules granted")
        return
    
    # Check if this is an Admin group
    if group.name.lower() == "admin":
        # Admin gets all modules with all their headings
        try:
            modules = Module.objects.all()
            created_count = 0
            for module in modules:
                UserModuleProvision.objects.create(
                    user=user,
                    module_name=module.name,
                    headings=module.headings or []
                )
                created_count += 1
            logger.info(f"[ModuleAssignment] Admin user {user.username} granted access to {created_count} modules")
        except Exception as e:
            logger.error(f"[ModuleAssignment] Error assigning modules to admin {user.username}: {str(e)}")
    else:
        # Non-admin groups: only get modules explicitly linked to that group
        try:
            modules = Module.objects.filter(groups=group)
            created_count = 0
            for module in modules:
                UserModuleProvision.objects.create(
                    user=user,
                    module_name=module.name,
                    headings=module.headings or []
                )
                created_count += 1
            logger.info(f"[ModuleAssignment] User {user.username} ({group.name}) granted access to {created_count} module(s): {[m.name for m in modules]}")
        except Exception as e:
            logger.error(f"[ModuleAssignment] Error assigning modules to {user.username}: {str(e)}")'''

# Define the new function
new_func = '''def assign_modules_to_user_by_group(user, group):
    """
    Automatically assign modules to a user based on their user category (group).
    Hardcoded module mappings for specific categories ensure correct assignments:
    - Admin: All modules
    - DP User: Data Upload, DP Pick Table, DP Complete Table
    - IS User: Input Screening
    - BQC User: Brass QC
    - IQF User: IQF
    - BA User: Brass Audit
    """
    from django.contrib.auth.models import Group
    
    # Hardcoded module mappings for specific user categories
    GROUP_MODULE_MAP = {
        "DP User": ["Data Upload", "DP Pick Table", "DP Complete Table"],
        "DP-User": ["Data Upload", "DP Pick Table", "DP Complete Table"],
        "IS User": ["Input Screening"],
        "BQC User": ["Brass QC"],
        "IQF User": ["IQF"],
        "BA User": ["Brass Audit"],
    }
    
    # Clear all existing module provisions for this user
    UserModuleProvision.objects.filter(user=user).delete()
    
    if not group:
        logger.info(f"[ModuleAssignment] User {user.username} has no group assigned, no modules granted")
        return
    
    # Check if this is an Admin group
    if group.name.lower() == "admin":
        # Admin gets all modules with all their headings
        try:
            modules = Module.objects.all()
            created_count = 0
            for module in modules:
                UserModuleProvision.objects.create(
                    user=user,
                    module_name=module.name,
                    headings=module.headings or []
                )
                created_count += 1
            logger.info(f"[ModuleAssignment] Admin user {user.username} granted access to {created_count} modules")
        except Exception as e:
            logger.error(f"[ModuleAssignment] Error assigning modules to admin {user.username}: {str(e)}")
    else:
        # Try to get modules from hardcoded mapping first
        module_names_to_assign = GROUP_MODULE_MAP.get(group.name)
        
        if module_names_to_assign:
            # Use hardcoded mapping for DP User, IS User, etc.
            try:
                modules = Module.objects.filter(name__in=module_names_to_assign)
                created_count = 0
                for module in modules:
                    UserModuleProvision.objects.create(
                        user=user,
                        module_name=module.name,
                        headings=module.headings or []
                    )
                    created_count += 1
                logger.info(f"[ModuleAssignment] User {user.username} ({group.name}) granted access to {created_count} module(s): {list(modules.values_list('name', flat=True))}")
            except Exception as e:
                logger.error(f"[ModuleAssignment] Error assigning modules to {user.username}: {str(e)}")
        else:
            # Fallback: try to get modules from Module.groups relationship
            try:
                modules = Module.objects.filter(groups=group)
                created_count = 0
                for module in modules:
                    UserModuleProvision.objects.create(
                        user=user,
                        module_name=module.name,
                        headings=module.headings or []
                    )
                    created_count += 1
                if created_count > 0:
                    logger.info(f"[ModuleAssignment] User {user.username} ({group.name}) granted access to {created_count} module(s) via group relationship")
                else:
                    logger.warning(f"[ModuleAssignment] No modules found for group {group.name}. User {user.username} has no module access.")
            except Exception as e:
                logger.error(f"[ModuleAssignment] Error assigning modules to {user.username}: {str(e)}")'''

# Replace the function
content = content.replace(old_func, new_func)

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ assign_modules_to_user_by_group function updated successfully!")
