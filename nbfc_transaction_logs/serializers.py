from rest_framework import serializers
from .models import TransactionLog
from nbfc_accounts.serializers import UserSerializer

class TransactionLogSerializer(serializers.ModelSerializer):
    performed_by = UserSerializer(read_only=True)

    class Meta:
        model = TransactionLog
        fields = [
            'id', 'organization', 'transaction_type', 'description',
            'old_data', 'new_data', 'performed_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class TransactionLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = [
            'organization', 'transaction_type', 'description',
            'old_data', 'new_data'
        ] 