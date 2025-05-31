from rest_framework import serializers
from .models import Document
from nbfc_loans.serializers import LoanSerializer
from nbfc_accounts.serializers import UserSerializer

class DocumentSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_rejected = serializers.BooleanField(read_only=True)
    file_name = serializers.CharField(read_only=True)
    file_extension = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = (
            'id', 'loan', 'document_type', 'file', 'description',
            'status', 'verified_by', 'verified_at', 'verification_notes',
            'created_at', 'updated_at', 'is_verified', 'is_rejected',
            'file_name', 'file_extension'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'loan', 'document_type', 'file', 'description'
        )

class DocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'status', 'verified_by', 'verification_notes'
        ) 