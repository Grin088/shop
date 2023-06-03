from django.shortcuts import render  # noqa F401
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from .services import banner
from .services.catalog import get_featured_categories
# from .services.limited_products import get_random_limited_edition_product
from .services.limited_products import time_left  # пока не может использоваться из-за celery


@cache_page(settings.CACHE_CONSTANT)
def home(request):
    if request.method == "GET":
        featured_categories = get_featured_categories()
        random_banners = banner.banner()
        time_and_products = time_left()  # пока не может использоваться из-за celery
        update_time = time_and_products['time_left']  # пока не может использоваться из-за celery
        limited_products = time_and_products['limited_products']  # пока не может использоваться из-за celery
        # limited_products = get_random_limited_edition_product()

        context = {
            'featured_categories': featured_categories,
            'random_banners': random_banners,
            'update_time': update_time,  # пока не может использоваться из-за celery
            'limited_products': limited_products,
        }
        return render(request, 'market/index.jinja2', context=context)


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'
