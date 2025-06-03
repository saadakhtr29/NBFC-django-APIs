from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'document_type', 'uploaded_by_user', 'created_at')
    list_filter = ('document_type', 'created_at')
    search_fields = ('document_name', 'description')
    ordering = ('-created_at',)
