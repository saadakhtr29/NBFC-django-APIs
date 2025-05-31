from rest_framework import serializers
from .models import LoanDeficit, LoanExcess
from nbfc_employees.serializers import EmployeeSerializer
from nbfc_loans.serializers import LoanSerializer

class LoanDeficitSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    loan = LoanSerializer(read_only=True)
    approved_by = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = LoanDeficit
        fields = [
            'id', 'organization', 'employee', 'loan', 'amount', 'reason',
            'status', 'approved_by', 'approved_at', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['approved_by', 'approved_at', 'created_by', 'created_at', 'updated_at']

    def get_approved_by(self, obj):
        if obj.approved_by:
            return {
                'id': obj.approved_by.id,
                'username': obj.approved_by.username,
                'email': obj.approved_by.email
            }
        return None

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'id': obj.created_by.id,
                'username': obj.created_by.username,
                'email': obj.created_by.email
            }
        return None

class LoanDeficitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDeficit
        fields = ['organization', 'employee', 'loan', 'amount', 'reason']

class LoanDeficitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDeficit
        fields = ['amount', 'reason']

class LoanExcessSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    loan = LoanSerializer(read_only=True)
    approved_by = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = LoanExcess
        fields = [
            'id', 'organization', 'employee', 'loan', 'amount', 'reason',
            'status', 'approved_by', 'approved_at', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['approved_by', 'approved_at', 'created_by', 'created_at', 'updated_at']

    def get_approved_by(self, obj):
        if obj.approved_by:
            return {
                'id': obj.approved_by.id,
                'username': obj.approved_by.username,
                'email': obj.approved_by.email
            }
        return None

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'id': obj.created_by.id,
                'username': obj.created_by.username,
                'email': obj.created_by.email
            }
        return None

class LoanExcessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanExcess
        fields = ['organization', 'employee', 'loan', 'amount', 'reason']

class LoanExcessUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanExcess
        fields = ['amount', 'reason'] 