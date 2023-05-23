from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='users_register'),
    path('login/', views.MyLoginView.as_view(), name='users_login'),
    path('logout/', views.UserLogoutView.as_view(), name='users_logout'),
    # path('password/', views.RestorePasswordView.as_view(), name='users_restore_password'),
#     # path('profile/<int:id>/', , name='user_profile'),
#     # path('<id>/orders-history/'),
#     # path('<id>/product-browsing-history/'),
]
