from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App endpoints
    path('api/accounts/', include('nbfc_accounts.urls')),
    path('api/organizations/', include('nbfc_organizations.urls')),
    path('api/employees/', include('nbfc_employees.urls')),
    path('api/loans/', include('nbfc_loans.urls')),
    path('api/repayments/', include('nbfc_repayments.urls')),
    path('api/attendance/', include('nbfc_attendance.urls')),
    path('api/salaries/', include('nbfc_salaries.urls')),
    path('api/documents/', include('nbfc_documents.urls')),
    path('api/settings/', include('nbfc_settings.urls')),
    path('api/bulk-upload/', include('nbfc_bulk_upload.urls')),
    path('api/dashboard/', include('nbfc_dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 