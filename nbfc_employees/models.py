from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_accounts.models import User
from nbfc_organizations.models import Organization, Department

class Employee(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    MARITAL_STATUS = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def current_loans(self):
        return self.loans.filter(status__in=['approved', 'disbursed'])

    @property
    def total_loan_amount(self):
        return sum(loan.amount for loan in self.current_loans)

    @property
    def total_repayment_amount(self):
        return sum(repayment.amount for loan in self.loans.all() for repayment in loan.repayments.all())
