from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('organization/login/', views.OrganizationLoginView.as_view(), name='organization-login'),
    path('user/', views.UserView.as_view(), name='user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 