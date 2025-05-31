from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_accounts.models import User
from nbfc_employees.models import Employee
from nbfc_organizations.models import Organization

class Loan(models.Model):
    LOAN_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('completed', 'Completed'),
        ('defaulted', 'Defaulted'),
    )

    LOAN_TYPE = (
        ('personal', 'Personal'),
        ('business', 'Business'),
        ('education', 'Education'),
        ('home', 'Home'),
        ('vehicle', 'Vehicle'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='loans')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    purpose = models.TextField()
    disbursement_date = models.DateField(null=True, blank=True)
    next_payment_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_loans')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_loans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Loan')
        verbose_name_plural = _('Loans')

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.loan_type} Loan"

    @property
    def total_amount(self):
        return self.amount + (self.amount * self.interest_rate / 100)

    @property
    def monthly_payment(self):
        if self.term_months > 0:
            return self.total_amount / self.term_months
        return 0

    @property
    def remaining_amount(self):
        total_paid = sum(repayment.amount for repayment in self.repayments.all())
        return self.total_amount - total_paid

    @property
    def remaining_months(self):
        if self.term_months > 0:
            return self.term_months - self.repayments.count()
        return 0
