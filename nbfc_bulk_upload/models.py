from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_organizations.models import Organization
from django.conf import settings

class BulkUpload(models.Model):
    UPLOAD_TYPES = (
        ('employees', _('Employees')),
        ('loans', _('Loans')),
        ('attendance', _('Attendance')),
        ('salaries', _('Salaries')),
    )

    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bulk_uploads')
    upload_type = models.CharField(max_length=20, choices=UPLOAD_TYPES)
    file = models.FileField(upload_to='bulk_uploads/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_records = models.IntegerField(default=0)
    processed_records = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    error_log = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_uploads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Bulk Upload')
        verbose_name_plural = _('Bulk Uploads')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.upload_type} - {self.created_at}" 