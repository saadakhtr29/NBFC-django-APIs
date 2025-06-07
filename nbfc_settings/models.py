from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_organizations.models import Organization
from nbfc_accounts.models import User

class OrganizationSetting(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_settings')
    key = models.CharField(max_length=100)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_org_settings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']
        unique_together = ['organization', 'key']
        verbose_name = _('Organization Setting')
        verbose_name_plural = _('Organization Settings')

    def __str__(self):
        return f"{self.organization.name} - {self.key}"

class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_system_settings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']
        verbose_name = _('System Setting')
        verbose_name_plural = _('System Settings')

    def __str__(self):
        return self.key

class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'nbfc_settings'
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
