from django.shortcuts import render  # noqa F401
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from .services.banner import banner
from .services.catalog import get_featured_categories


@cache_page(settings.CACHE_CONSTANT)
def home(request):
    featured_categories = get_featured_categories()
    random_banners = banner()
    context = {
        'featured_categories': featured_categories,
        'random_banners': random_banners,
    }
    return render(request, 'market/index.jinja2', context=context)


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'
