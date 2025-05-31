from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'organization-settings', views.OrganizationSettingViewSet)
router.register(r'system-settings', views.SystemSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 