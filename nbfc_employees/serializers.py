from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Employee
from nbfc_accounts.serializers import UserSerializer

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_loans = serializers.IntegerField(read_only=True)
    total_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_repayment_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Employee
        fields = (
            'id', 'user', 'organization', 'department', 'employee_id',
            'first_name', 'last_name', 'email', 'phone', 'address',
            'date_of_birth', 'gender', 'marital_status', 'joining_date',
            'salary', 'is_active', 'current_loans', 'total_loan_amount',
            'total_repayment_amount', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class EmployeeCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = (
            'user', 'organization', 'department', 'employee_id',
            'first_name', 'last_name', 'email', 'phone', 'address',
            'date_of_birth', 'gender', 'marital_status', 'joining_date',
            'salary', 'is_active'
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'department', 'phone', 'address', 'marital_status',
            'salary', 'is_active'
        )

class EmployeeBulkCreateSerializer(serializers.Serializer):
    employees = EmployeeCreateSerializer(many=True) 