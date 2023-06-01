from django.urls import path
from .views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('', BaseView.as_view(), name='login'),
    path('', BaseView.as_view(), name='registr'),
    path('', BaseView.as_view(), name='catalog'),
    path('', BaseView.as_view(), name='comparison'),
    path('', BaseView.as_view(), name='cart'),
    path('', BaseView.as_view(), name='account'),
]
