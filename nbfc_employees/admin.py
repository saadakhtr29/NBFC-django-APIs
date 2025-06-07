from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'email', 'department', 'organization', 'salary', 'is_active', 'joining_date')
    list_filter = ('is_active', 'gender', 'marital_status', 'department', 'organization')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('employee_id',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'marital_status')
        }),
        ('Employment Details', {
            'fields': ('user', 'organization', 'department', 'joining_date', 'salary', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
