from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import TransactionLog
from .serializers import TransactionLogSerializer, TransactionLogCreateSerializer

class TransactionLogFilter(filters.FilterSet):
    organization = filters.NumberFilter(field_name='organization__id')
    transaction_type = filters.CharFilter(field_name='transaction_type')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = TransactionLog
        fields = ['organization', 'transaction_type', 'created_at']

class TransactionLogViewSet(viewsets.ModelViewSet):
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionLogFilter
    search_fields = ['description']
    ordering_fields = ['transaction_type', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionLogCreateSerializer
        return TransactionLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_transactions = queryset.count()
        
        # Count by transaction type
        transaction_types = {}
        for transaction_type, _ in TransactionLog.TRANSACTION_TYPES:
            count = queryset.filter(transaction_type=transaction_type).count()
            transaction_types[transaction_type] = count

        # Count by organization
        organization_stats = {}
        for org in queryset.values_list('organization', flat=True).distinct():
            count = queryset.filter(organization=org).count()
            organization_stats[org] = count

        return Response({
            'total_transactions': total_transactions,
            'by_type': transaction_types,
            'by_organization': organization_stats
        })

    @action(detail=False, methods=['get'])
    def loan_transactions(self, request):
        loan_id = request.query_params.get('loan_id')
        if not loan_id:
            return Response(
                {'error': 'Loan ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            transaction_type__in=[
                'loan_created', 'loan_updated', 'loan_approved',
                'loan_rejected', 'loan_disbursed'
            ],
            new_data__contains={'loan_id': int(loan_id)}
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 