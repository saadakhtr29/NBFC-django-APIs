from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = 'organizations'

router = DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet, basename='organization')
router.register(r'departments', views.DepartmentViewSet, basename='department')

urlpatterns = [
    # Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Organization management
    # path('register/', views.OrganizationCreateView.as_view(), name='organization_create'),
    path('list/', views.OrganizationListView.as_view(), name='organization_list'),
    path('<int:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('<int:pk>/update/', views.OrganizationUpdateView.as_view(), name='organization_update'),
    path('<int:pk>/change-password/', views.ChangeOrganizationPasswordView.as_view(), name='organization_change_password'),
    # path('<int:pk>/statistics/', views.OrganizationStatisticsView.as_view(), name='organization_statistics'),
    path('', include(router.urls)),
] 