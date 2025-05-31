from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_employees.models import Employee
from nbfc_accounts.models import User

class Salary(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    month = models.DateField()  # Store as first day of the month
    basic_salary = models.DecimalField(max_digits=15, decimal_places=2)
    allowances = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    overtime = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_salaries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-month']
        unique_together = ['employee', 'month']
        verbose_name = _('Salary')
        verbose_name_plural = _('Salaries')

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.month.strftime('%B %Y')}"

    @property
    def total_earnings(self):
        return self.basic_salary + self.allowances + self.bonus + self.overtime

    @property
    def net_salary(self):
        return self.total_earnings - self.deductions

    @property
    def is_paid(self):
        return self.status == 'paid'

    @property
    def is_approved(self):
        return self.status in ['approved', 'paid']
