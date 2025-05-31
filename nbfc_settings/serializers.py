from rest_framework import serializers
from .models import OrganizationSetting, SystemSetting
from nbfc_accounts.serializers import UserSerializer

class OrganizationSettingSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationSetting
        fields = (
            'id', 'organization', 'key', 'value', 'description',
            'is_active', 'created_by', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class OrganizationSettingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        fields = (
            'organization', 'key', 'value', 'description', 'is_active'
        )

class OrganizationSettingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        fields = (
            'value', 'description', 'is_active'
        )

class SystemSettingSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = SystemSetting
        fields = (
            'id', 'key', 'value', 'description',
            'is_active', 'created_by', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class SystemSettingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = (
            'key', 'value', 'description', 'is_active'
        )

class SystemSettingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = (
            'value', 'description', 'is_active'
        ) 