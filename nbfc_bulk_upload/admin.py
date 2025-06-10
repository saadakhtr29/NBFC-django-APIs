from django.contrib import admin
from django.utils.html import format_html
from .models import BulkUpload

@admin.register(BulkUpload)
class BulkUploadAdmin(admin.ModelAdmin):
    list_display = (
        'upload_type', 'organization', 'status', 'total_records', 
        'success_count', 'failure_count', 'progress_display', 
        'created_by', 'created_at'
    )
    list_filter = ('status', 'upload_type', 'created_at', 'organization')
    search_fields = ('upload_type', 'organization__name', 'created_by__username')
    readonly_fields = (
        'status', 'total_records', 'processed_records', 'success_count', 
        'failure_count', 'error_log', 'created_at', 'updated_at'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Upload Information', {
            'fields': ('organization', 'upload_type', 'file', 'created_by')
        }),
        ('Processing Status', {
            'fields': ('status', 'total_records', 'processed_records', 'success_count', 'failure_count')
        }),
        ('Error Details', {
            'fields': ('error_log',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def progress_display(self, obj):
        if obj.total_records > 0:
            progress = (obj.processed_records / obj.total_records) * 100
            color = 'green' if progress == 100 else 'orange' if progress > 0 else 'red'
            return format_html(
                '<span style="color: {};">{:.1f}%</span>',
                color,
                progress
            )
        return "0%"
    progress_display.short_description = 'Progress'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            # Filter by user's organization if not superuser
            if hasattr(request.user, 'organization'):
                queryset = queryset.filter(organization=request.user.organization)
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
