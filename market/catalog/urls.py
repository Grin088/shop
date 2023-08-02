from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ViewShows


app_name = "catalog"

urlpatterns = [
    path("", cache_page(settings.CACHE_TIME_PER_DAY, key_prefix='catalog')(ViewShows.as_view()), name="show_product"),
]
