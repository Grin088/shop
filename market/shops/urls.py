from django.urls import path
from .views import (BaseView,
                    seller_detail,
                    home,
                    ComparePageView,
                    OrderView,
                    OrderLoginView,
                    HistoryOrderView,
                    OrderDetailsView,
                    )


app_name = "shops"

urlpatterns = [
    path('', BaseView.as_view(), name='index'),
    path('', BaseView.as_view(), name='login'),
    path('', BaseView.as_view(), name='registr'),
    path('', BaseView.as_view(), name='catalog'),
    path('comparison/', ComparePageView.as_view(), name='comparison'),
    path('', BaseView.as_view(), name='cart'),
    path('', BaseView.as_view(), name='account'),
    path('home/', home, name='home'),
    path('seller/', seller_detail, name='seller_detail'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/login/', OrderLoginView.as_view(), name='order_login'),
    path('order_history/', HistoryOrderView.as_view(), name='order_history'),
    path('order_history/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
]
