from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import LoanRepayment
from .serializers import (
    LoanRepaymentSerializer, LoanRepaymentCreateSerializer, LoanRepaymentUpdateSerializer
)

# Create your views here.

class LoanRepaymentFilter(filters.FilterSet):
    loan = filters.NumberFilter(field_name='loan__id')
    payment_date = filters.DateFilter(field_name='payment_date')
    status = filters.CharFilter(field_name='status')
    payment_method = filters.CharFilter(field_name='payment_method')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = LoanRepayment
        fields = ['loan', 'payment_date', 'status', 'payment_method', 'created_at']

class LoanRepaymentViewSet(viewsets.ModelViewSet):
    queryset = LoanRepayment.objects.all()
    serializer_class = LoanRepaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LoanRepaymentFilter
    search_fields = ['loan__employee__first_name', 'loan__employee__last_name', 'notes']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanRepaymentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LoanRepaymentUpdateSerializer
        return LoanRepaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(loan__organization=self.request.user.organization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_repayments = queryset.count()
        total_amount = queryset.aggregate(total=filters.models.Sum('amount'))['total'] or 0
        approved = queryset.filter(status='approved').count()
        pending = queryset.filter(status='pending').count()
        completed = queryset.filter(status='completed').count()
        rejected = queryset.filter(status='rejected').count()
        return Response({
            'total_repayments': total_repayments,
            'total_amount': total_amount,
            'approved': approved,
            'pending': pending,
            'completed': completed,
            'rejected': rejected
        })
