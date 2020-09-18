from django.urls import path
from  .import views
from accounts.views import RegistrationView


urlpatterns = [

    path('accounts/register/', RegistrationView.as_view(), name='register'),
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login_view, name='login'),
    path('accounts/logout/', views.user_logout_view, name='logout'),


    path('accounts/api/profile', views.profile, name='api_profile'),
    path('accounts/api/login', views.login_view, name='api_login'),
    path("accounts/api/register", views.registration_view, name="api_register")

]