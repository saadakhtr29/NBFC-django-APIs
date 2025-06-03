from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'loan_type', 'amount', 'interest_rate', 'status', 'disbursement_date', 'remaining_amount')
    list_filter = ('loan_type', 'status', 'organization')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    ordering = ('-created_at',)
    readonly_fields = ('total_amount', 'monthly_payment', 'remaining_amount', 'remaining_months', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Loan Information', {
            'fields': ('employee', 'organization', 'loan_type', 'purpose')
        }),
        ('Loan Terms', {
            'fields': ('amount', 'interest_rate', 'term_months')
        }),
        ('Calculated Fields', {
            'fields': ('total_amount', 'monthly_payment', 'remaining_amount', 'remaining_months'),
            'classes': ('collapse',)
        }),
        ('Status & Dates', {
            'fields': ('status', 'disbursement_date', 'next_payment_date')
        }),
        ('Approval Information', {
            'fields': ('created_by', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        if not obj.approved_by and obj.status == 'approved':
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)
