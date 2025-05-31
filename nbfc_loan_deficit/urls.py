from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'deficits', views.LoanDeficitViewSet)
router.register(r'excesses', views.LoanExcessViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 