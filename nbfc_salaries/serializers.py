from rest_framework import serializers
from .models import Salary
from nbfc_employees.serializers import EmployeeSerializer
from nbfc_accounts.serializers import UserSerializer

class SalarySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    total_earnings = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    net_salary = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    is_paid = serializers.BooleanField(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Salary
        fields = (
            'id', 'employee', 'month', 'basic_salary', 'allowances',
            'deductions', 'bonus', 'overtime', 'status', 'payment_date',
            'payment_method', 'transaction_reference', 'notes', 'approved_by',
            'created_at', 'updated_at', 'total_earnings', 'net_salary',
            'is_paid', 'is_approved'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class SalaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = (
            'employee', 'month', 'basic_salary', 'allowances',
            'deductions', 'bonus', 'overtime', 'notes'
        )

class SalaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = (
            'status', 'payment_date', 'payment_method',
            'transaction_reference', 'notes', 'approved_by'
        ) 