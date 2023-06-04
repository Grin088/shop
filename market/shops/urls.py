from django.urls import path
<<<<<<< HEAD
from .views import BaseView, home
=======
from .views import BaseView, seller_detail
>>>>>>> develop

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('', BaseView.as_view(), name='login'),
    path('', BaseView.as_view(), name='registr'),
    path('', BaseView.as_view(), name='catalog'),
    path('', BaseView.as_view(), name='comparison'),
    path('', BaseView.as_view(), name='cart'),
    path('', BaseView.as_view(), name='account'),
<<<<<<< HEAD
    path('home/', home, name='home'),
=======
    path('seller/', seller_detail, name='seller_detail'),
>>>>>>> develop
]
