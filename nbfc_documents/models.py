from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_loans.models import Loan
from nbfc_accounts.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    DOCUMENT_TYPE = (
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
        ('income_proof', 'Income Proof'),
        ('bank_statement', 'Bank Statement'),
        ('loan_agreement', 'Loan Agreement'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE)
    file = models.FileField(upload_to='loan_documents/')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        db_table = 'nbfc_documents'

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.loan}"

    @property
    def is_verified(self):
        return self.status == 'verified'

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    @property
    def file_name(self):
        return self.file.name.split('/')[-1]

    @property
    def file_extension(self):
        return self.file_name.split('.')[-1].lower()
