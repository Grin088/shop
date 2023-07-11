from django.views import View
from catalog import services


class ViewShows(services.MixinGetPost, View):
    pass
