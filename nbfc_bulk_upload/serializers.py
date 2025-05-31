from rest_framework import serializers
from .models import BulkUpload
from nbfc_accounts.serializers import UserSerializer

class BulkUploadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = BulkUpload
        fields = [
            'id', 'organization', 'upload_type', 'file', 'status',
            'total_records', 'processed_records', 'success_count',
            'failure_count', 'error_log', 'created_by', 'created_at',
            'updated_at', 'progress'
        ]
        read_only_fields = [
            'id', 'status', 'total_records', 'processed_records',
            'success_count', 'failure_count', 'error_log', 'created_by',
            'created_at', 'updated_at'
        ]

    def get_progress(self, obj):
        if obj.total_records > 0:
            return (obj.processed_records / obj.total_records) * 100
        return 0

class BulkUploadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkUpload
        fields = ['organization', 'upload_type', 'file'] 