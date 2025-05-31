from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from nbfc_django.base_views import BaseModelViewSet
from .models import Employee
from .serializers import (
    EmployeeSerializer, EmployeeCreateSerializer,
    EmployeeUpdateSerializer, EmployeeBulkCreateSerializer
)

# Create your views here.

class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'employee_id': ['exact'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'gender': ['exact'],
            'marital_status': ['exact'],
            'is_active': ['exact'],
            'joining_date': ['gte', 'lte'],
            'created_at': ['gte', 'lte'],
        }

class EmployeeViewSet(BaseModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EmployeeFilter
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['employee_id', 'first_name', 'last_name', 'joining_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EmployeeUpdateSerializer
        return EmployeeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            return queryset.filter(organization=self.request.user.organization)
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = EmployeeBulkCreateSerializer(data=request.data)
        if serializer.is_valid():
            employees = serializer.save()
            return Response(
                EmployeeSerializer(employees, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        return Response({
            'total_employees': queryset.count(),
            'active_employees': queryset.filter(is_active=True).count(),
            'total_loans': sum(employee.current_loans.count() for employee in queryset),
            'total_loan_amount': sum(employee.total_loan_amount for employee in queryset),
            'total_repayment_amount': sum(employee.total_repayment_amount for employee in queryset),
        })
