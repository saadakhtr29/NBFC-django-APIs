from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'widgets', views.DashboardWidgetViewSet)
router.register(r'reports', views.SavedReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 