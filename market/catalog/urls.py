from django.urls import path

from catalog.views import ViewShows

app_name = "catalog"


urlpatterns = [
    path('', ViewShows.as_view(), name='show_product'),

]
