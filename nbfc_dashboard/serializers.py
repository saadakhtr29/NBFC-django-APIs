from rest_framework import serializers
from .models import DashboardWidget, SavedReport
from nbfc_auth.serializers import UserSerializer

class DashboardWidgetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'organization', 'user', 'name', 'widget_type',
            'config', 'position', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

class DashboardWidgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = [
            'organization', 'name', 'widget_type', 'config', 'position'
        ]

class DashboardWidgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = [
            'name', 'config', 'position', 'is_active'
        ]

class SavedReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SavedReport
        fields = [
            'id', 'organization', 'user', 'name', 'report_type',
            'config', 'schedule', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

class SavedReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = [
            'organization', 'name', 'report_type', 'config',
            'schedule', 'is_public'
        ]

class SavedReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = [
            'name', 'config', 'schedule', 'is_public'
        ] 