from django.urls import path

from .views import ViewShows

urlpatterns = [
    path('', ViewShows.as_view(), name='show_product')
]
