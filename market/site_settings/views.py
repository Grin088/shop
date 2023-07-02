from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect
from django.http import JsonResponse


def clear_all_cache_view(request):
    """Очистка всего кеша"""
    cache.clear()
    # messages.success(request, 'All cache is cleared')
    return JsonResponse({'status': 'ok'})
