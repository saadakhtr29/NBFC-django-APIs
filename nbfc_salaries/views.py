from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from nbfc_django.base_views import BaseModelViewSet
from .models import Salary
from .serializers import (
    SalarySerializer, SalaryCreateSerializer, SalaryUpdateSerializer
)

# Create your views here.

class SalaryFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee__id')
    month = filters.DateFilter(field_name='month')
    status = filters.CharFilter(field_name='status')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = Salary
        fields = ['employee', 'month', 'status', 'created_at']

class SalaryViewSet(BaseModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]
    filterset_class = SalaryFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'notes']
    ordering_fields = ['month', 'basic_salary', 'created_at']
    ordering = ['-month']

    def get_serializer_class(self):
        if self.action == 'create':
            return SalaryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SalaryUpdateSerializer
        return SalarySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__organization=self.request.user.organization)
        return queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        salary = self.get_object()
        salary.status = 'approved'
        salary.approved_by = request.user
        salary.save()
        return Response(SalarySerializer(salary).data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_salaries = queryset.count()
        total_amount = queryset.aggregate(total=filters.models.Sum('net_salary'))['total'] or 0
        approved = queryset.filter(status='approved').count()
        pending = queryset.filter(status='pending').count()
        paid = queryset.filter(status='paid').count()
        rejected = queryset.filter(status='rejected').count()
        return Response({
            'total_salaries': total_salaries,
            'total_amount': total_amount,
            'approved': approved,
            'pending': pending,
            'paid': paid,
            'rejected': rejected
        })
