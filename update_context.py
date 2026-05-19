#!/usr/bin/env python
"""Script to update context_processors.py with role-based access control"""

path = r'c:\Users\athit\TTT-Dev\adminportal\context_processors.py'

content = """from django.core.cache import cache
from adminportal.models import UserModuleProvision, Module
import logging

logger = logging.getLogger(__name__)

# Cache key and TTL for module list (same for all authenticated users)
_MODULE_CACHE_KEY = 'all_module_names'
_MODULE_CACHE_TTL = 300  # 5 minutes


def user_permissions(request):
    \"\"\"
    Add user permission context to all templates.
    Respects role-based access control:
    - Admin users: see all modules
    - Regular users: see only modules assigned to their group via UserModuleProvision
    \"\"\"
    if request.user.is_authenticated:
        is_admin = request.user.is_superuser or request.user.groups.filter(name__iexact=\"Admin\").exists()
        
        try:
            if is_admin:
                # Admin users see all modules (use cache)
                allowed_modules = cache.get(_MODULE_CACHE_KEY)
                if allowed_modules is None:
                    allowed_modules = list(Module.objects.values_list('name', flat=True))
                    cache.set(_MODULE_CACHE_KEY, allowed_modules, _MODULE_CACHE_TTL)
            else:
                # Regular users see only modules assigned to their group
                # No caching for per-user provisions as they vary by user
                provisions = UserModuleProvision.objects.filter(user=request.user)
                allowed_modules = list(provisions.values_list('module_name', flat=True).distinct())
        except Exception as e:
            logger.error(f\"[ContextProcessor] Error getting modules for {request.user.username}: {str(e)}\")
            allowed_modules = []

        return {
            'is_admin': is_admin,
            'allowed_modules': allowed_modules,
        }

    return {
        'is_admin': False,
        'allowed_modules': [],
    }
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Context processor updated successfully!")
