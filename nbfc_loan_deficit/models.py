from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_organizations.models import Organization
from nbfc_employees.models import Employee
from nbfc_loans.models import Loan
from django.conf import settings

class LoanDeficit(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='loan_deficits')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='loan_deficits')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='deficits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_deficits')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_deficits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Loan Deficit')
        verbose_name_plural = _('Loan Deficits')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee} - {self.amount}"

class LoanExcess(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='loan_excesses')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='loan_excesses')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='excesses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_excesses')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_excesses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Loan Excess')
        verbose_name_plural = _('Loan Excesses')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee} - {self.amount}" 