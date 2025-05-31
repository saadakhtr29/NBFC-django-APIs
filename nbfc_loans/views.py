from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db.models import Sum, Count
from nbfc_django.base_views import BaseModelViewSet
from .models import Loan
from .serializers import (
    LoanSerializer, LoanCreateSerializer,
    LoanUpdateSerializer, LoanBulkCreateSerializer
)

# Create your views here.

class LoanFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee__id')
    organization = filters.NumberFilter(field_name='organization__id')
    loan_type = filters.CharFilter(field_name='loan_type')
    status = filters.CharFilter(field_name='status')
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    min_interest_rate = filters.NumberFilter(field_name='interest_rate', lookup_expr='gte')
    max_interest_rate = filters.NumberFilter(field_name='interest_rate', lookup_expr='lte')
    disbursement_date = filters.DateFilter(field_name='disbursement_date')
    next_payment_date = filters.DateFilter(field_name='next_payment_date')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = Loan
        fields = [
            'employee', 'organization', 'loan_type', 'status',
            'min_amount', 'max_amount', 'min_interest_rate',
            'max_interest_rate', 'disbursement_date',
            'next_payment_date', 'created_at'
        ]

class LoanViewSet(BaseModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LoanFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'purpose']
    ordering_fields = ['amount', 'interest_rate', 'term_months', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LoanUpdateSerializer
        return LoanSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = LoanBulkCreateSerializer(data=request.data)
        if serializer.is_valid():
            loans = serializer.validated_data['loans']
            created_loans = []
            for loan_data in loans:
                loan_data['created_by'] = request.user
                loan = Loan.objects.create(**loan_data)
                created_loans.append(loan)
            return Response(
                LoanSerializer(created_loans, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_loans = queryset.count()
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        total_interest = queryset.aggregate(total=Sum('interest_rate'))['total'] or 0
        active_loans = queryset.filter(status='active').count()
        pending_loans = queryset.filter(status='pending').count()
        completed_loans = queryset.filter(status='completed').count()
        rejected_loans = queryset.filter(status='rejected').count()

        return Response({
            'total_loans': total_loans,
            'total_amount': total_amount,
            'total_interest': total_interest,
            'active_loans': active_loans,
            'pending_loans': pending_loans,
            'completed_loans': completed_loans,
            'rejected_loans': rejected_loans
        })
