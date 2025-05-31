from rest_framework import serializers
from .models import Attendance
from nbfc_employees.serializers import EmployeeSerializer
from nbfc_accounts.serializers import UserSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_late = serializers.BooleanField(read_only=True)
    is_early_leave = serializers.BooleanField(read_only=True)

    class Meta:
        model = Attendance
        fields = (
            'id', 'employee', 'date', 'status', 'check_in', 'check_out',
            'working_hours', 'notes', 'verified_by', 'verified_at',
            'created_at', 'updated_at', 'is_verified', 'is_late', 'is_early_leave'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'employee', 'date', 'status', 'check_in', 'check_out',
            'working_hours', 'notes'
        )

class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'status', 'check_in', 'check_out', 'working_hours', 'notes'
        ) 