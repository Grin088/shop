from django.views import View
from product_catalog import services


class ViewShows(services.MixinGetPost, View):
    pass

