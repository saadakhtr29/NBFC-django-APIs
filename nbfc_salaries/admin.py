from django.contrib import admin
from .models import Salary

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'basic_salary', 'net_salary', 'status', 'payment_date')
    list_filter = ('status', 'month', 'payment_method')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    ordering = ('-month',)
    readonly_fields = ('total_earnings', 'net_salary', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Employee & Period', {
            'fields': ('employee', 'month')
        }),
        ('Salary Components', {
            'fields': ('basic_salary', 'allowances', 'bonus', 'overtime', 'deductions')
        }),
        ('Calculated Fields', {
            'fields': ('total_earnings', 'net_salary'),
            'classes': ('collapse',)
        }),
        ('Payment Information', {
            'fields': ('status', 'payment_date', 'payment_method', 'transaction_reference')
        }),
        ('Approval & Notes', {
            'fields': ('approved_by', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change and not obj.approved_by and obj.status == 'approved':
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)
