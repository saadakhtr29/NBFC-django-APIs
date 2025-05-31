from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'salaries', views.SalaryViewSet, basename='salary')

urlpatterns = [
    path('', include(router.urls)),
] 