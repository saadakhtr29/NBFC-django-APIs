from rest_framework import serializers
from .models import LoanRepayment
from nbfc_loans.serializers import LoanSerializer
from nbfc_accounts.serializers import UserSerializer

class LoanRepaymentSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    is_late = serializers.BooleanField(read_only=True)
    days_late = serializers.IntegerField(read_only=True)

    class Meta:
        model = LoanRepayment
        fields = (
            'id', 'loan', 'amount', 'payment_date', 'payment_method',
            'status', 'transaction_reference', 'notes', 'created_by',
            'approved_by', 'created_at', 'updated_at', 'is_late', 'days_late'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class LoanRepaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = (
            'loan', 'amount', 'payment_date', 'payment_method',
            'notes'
        )

class LoanRepaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = (
            'status', 'approved_by', 'transaction_reference', 'notes'
        ) 