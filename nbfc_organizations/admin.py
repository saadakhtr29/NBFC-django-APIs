from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'status', 'city', 'state', 'country')
    search_fields = ('name', 'code', 'city', 'state', 'country')
    list_filter = ('type', 'status', 'industry')
    ordering = ('name',)
    fieldsets = (
        ('Organization Info', {
            'fields': ('name', 'code', 'type', 'status')
        }),
        ('Contact Info', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code', 'phone', 'website')
        }),
        ('Business Info', {
            'fields': ('registration_number', 'tax_number', 'founding_date', 'industry', 'size', 'annual_revenue')
        }),
        ('Settings', {
            'fields': ('currency', 'timezone', 'settings', 'remarks')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new organization
            obj.user = request.user
        super().save_model(request, obj, form, change)
