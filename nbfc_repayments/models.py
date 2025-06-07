from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_loans.models import Loan
from nbfc_accounts.models import User

class LoanRepayment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('other', 'Other'),
    )

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_repayments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_repayments')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_repayments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('Loan Repayment')
        verbose_name_plural = _('Loan Repayments')

    def __str__(self):
        return f"Repayment for {self.loan} - {self.amount}"

    @property
    def is_late(self):
        return self.payment_date > self.loan.next_payment_date if self.loan.next_payment_date else False

    @property
    def days_late(self):
        if self.is_late and self.loan.next_payment_date:
            return (self.payment_date - self.loan.next_payment_date).days
        return 0

class Repayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.loan.employee} - {self.amount}"
    
    class Meta:
        db_table = 'nbfc_repayments'
        verbose_name = 'Repayment'
        verbose_name_plural = 'Repayments'
