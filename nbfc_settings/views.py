from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import OrganizationSetting, SystemSetting
from .serializers import (
    OrganizationSettingSerializer, OrganizationSettingCreateSerializer, OrganizationSettingUpdateSerializer,
    SystemSettingSerializer, SystemSettingCreateSerializer, SystemSettingUpdateSerializer
)

# Create your views here.

class OrganizationSettingFilter(filters.FilterSet):
    organization = filters.NumberFilter(field_name='organization__id')
    key = filters.CharFilter(field_name='key')
    is_active = filters.BooleanFilter(field_name='is_active')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = OrganizationSetting
        fields = ['organization', 'key', 'is_active', 'created_at']

class OrganizationSettingViewSet(viewsets.ModelViewSet):
    queryset = OrganizationSetting.objects.all()
    serializer_class = OrganizationSettingSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrganizationSettingFilter
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at']
    ordering = ['key']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrganizationSettingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrganizationSettingUpdateSerializer
        return OrganizationSettingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def get_by_key(self, request):
        key = request.query_params.get('key')
        if not key:
            return Response({'error': 'Key parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset().filter(key=key)
        if not queryset.exists():
            return Response({'error': 'Setting not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)

class SystemSettingFilter(filters.FilterSet):
    key = filters.CharFilter(field_name='key')
    is_active = filters.BooleanFilter(field_name='is_active')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = SystemSetting
        fields = ['key', 'is_active', 'created_at']

class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = SystemSettingFilter
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at']
    ordering = ['key']

    def get_serializer_class(self):
        if self.action == 'create':
            return SystemSettingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SystemSettingUpdateSerializer
        return SystemSettingSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def get_by_key(self, request):
        key = request.query_params.get('key')
        if not key:
            return Response({'error': 'Key parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset().filter(key=key)
        if not queryset.exists():
            return Response({'error': 'Setting not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)
