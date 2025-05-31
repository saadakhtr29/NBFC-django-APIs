from rest_framework import serializers
from .models import Loan
from nbfc_employees.serializers import EmployeeSerializer
from nbfc_organizations.serializers import OrganizationSerializer

class LoanSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    monthly_payment = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    remaining_months = serializers.IntegerField(read_only=True)

    class Meta:
        model = Loan
        fields = (
            'id', 'employee', 'organization', 'loan_type', 'amount',
            'interest_rate', 'term_months', 'status', 'purpose',
            'disbursement_date', 'next_payment_date', 'created_by',
            'approved_by', 'total_amount', 'monthly_payment',
            'remaining_amount', 'remaining_months', 'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            'employee', 'organization', 'loan_type', 'amount',
            'interest_rate', 'term_months', 'purpose'
        )

class LoanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            'status', 'disbursement_date', 'next_payment_date',
            'approved_by'
        )

class LoanBulkCreateSerializer(serializers.Serializer):
    loans = LoanCreateSerializer(many=True) 