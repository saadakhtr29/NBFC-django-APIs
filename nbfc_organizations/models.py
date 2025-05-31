from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from nbfc_accounts.models import User

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100, blank=True)
    tax_number = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='active')
    founding_date = models.DateField()
    industry = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50)
    settings = models.JSONField(default=dict)
    remarks = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_organizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    def __str__(self):
        return self.name or 'Unnamed Organization'

    @property
    def active_employees_count(self):
        return self.employees.filter(status='active').count()

    @property
    def active_loans_count(self):
        return self.loans.filter(status='active').count()

    @property
    def total_loan_amount(self):
        return sum(loan.amount for loan in self.loans.all())

    @property
    def total_repaid_amount(self):
        return sum(repayment.amount for loan in self.loans.all() for repayment in loan.repayments.all())

    @property
    def remaining_loan_amount(self):
        return self.total_loan_amount - self.total_repaid_amount

    @property
    def document_statistics(self):
        return {
            'total_documents': self.documents.count(),
            'documents_by_type': self.documents.values('type').annotate(count=models.Count('id'))
        }

    @property
    def total_employees(self):
        return self.employees.count()

    @property
    def total_loans(self):
        return self.loans.count()

    @property
    def total_repayment_amount(self):
        return sum(repayment.amount for loan in self.loans.all() for repayment in loan.repayments.all())

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['organization', 'code']
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return f"{self.organization.name} - {self.name}"

    @property
    def total_employees(self):
        return self.employees.count()
