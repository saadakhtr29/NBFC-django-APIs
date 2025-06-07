from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'document_type', 'status', 'created_at')
    list_filter = ('document_type', 'status', 'created_at')
    search_fields = ('description', 'loan__id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
