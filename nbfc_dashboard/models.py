from django.db import models
from django.contrib.auth import get_user_model
from nbfc_organizations.models import Organization

User = get_user_model()

class DashboardWidget(models.Model):
    WIDGET_TYPES = (
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('metric', 'Metric'),
        ('list', 'List'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    config = models.JSONField()
    position = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
        ordering = ['position']

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class SavedReport(models.Model):
    REPORT_TYPES = (
        ('loan', 'Loan Report'),
        ('employee', 'Employee Report'),
        ('attendance', 'Attendance Report'),
        ('salary', 'Salary Report'),
        ('custom', 'Custom Report'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    config = models.JSONField()
    schedule = models.JSONField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Saved Report'
        verbose_name_plural = 'Saved Reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}" 