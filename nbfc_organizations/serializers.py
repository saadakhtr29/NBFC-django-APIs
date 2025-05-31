from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, Department

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class OrganizationSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    total_employees = serializers.IntegerField(read_only=True)
    total_loans = serializers.IntegerField(read_only=True)
    total_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_repayment_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'code', 'address', 'phone', 'email', 'website',
            'logo', 'is_active', 'departments', 'total_employees',
            'total_loans', 'total_loan_amount', 'total_repayment_amount',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class OrganizationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new organization."""
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = Organization
        fields = (
            'name', 'code', 'address', 'phone', 'email', 'website',
            'logo', 'is_active', 'password', 'password_confirm'
        )

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')

        user = User.objects.create_user(
            email=email,
            password=password,
            user_type='organization'
        )

        organization = Organization.objects.create(
            user=user,
            **validated_data
        )
        return organization

class OrganizationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating organization information."""
    class Meta:
        model = Organization
        fields = (
            'name', 'address', 'phone', 'email', 'website',
            'logo', 'is_active'
        )
        read_only_fields = ('code',)

class ChangeOrganizationPasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return data 