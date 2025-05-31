from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.utils import timezone
from django.db import models
from .models import LoanDeficit, LoanExcess
from .serializers import (
    LoanDeficitSerializer, LoanDeficitCreateSerializer, LoanDeficitUpdateSerializer,
    LoanExcessSerializer, LoanExcessCreateSerializer, LoanExcessUpdateSerializer
)

class LoanDeficitFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee__id')
    loan = filters.NumberFilter(field_name='loan__id')
    status = filters.CharFilter(field_name='status')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = LoanDeficit
        fields = ['employee', 'loan', 'status', 'created_at']

class LoanDeficitViewSet(viewsets.ModelViewSet):
    queryset = LoanDeficit.objects.all()
    serializer_class = LoanDeficitSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LoanDeficitFilter
    search_fields = ['reason']
    ordering_fields = ['amount', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanDeficitCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LoanDeficitUpdateSerializer
        return LoanDeficitSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        deficit = self.get_object()
        if deficit.status != 'pending':
            return Response(
                {'error': 'Only pending deficits can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        deficit.status = 'approved'
        deficit.approved_by = request.user
        deficit.approved_at = timezone.now()
        deficit.save()
        serializer = self.get_serializer(deficit)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        deficit = self.get_object()
        if deficit.status != 'pending':
            return Response(
                {'error': 'Only pending deficits can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        deficit.status = 'rejected'
        deficit.approved_by = request.user
        deficit.approved_at = timezone.now()
        deficit.save()
        serializer = self.get_serializer(deficit)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_deficits = queryset.count()
        total_amount = queryset.aggregate(total=models.Sum('amount'))['total'] or 0
        pending_count = queryset.filter(status='pending').count()
        approved_count = queryset.filter(status='approved').count()
        rejected_count = queryset.filter(status='rejected').count()

        return Response({
            'total_deficits': total_deficits,
            'total_amount': total_amount,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count
        })

class LoanExcessFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee__id')
    loan = filters.NumberFilter(field_name='loan__id')
    status = filters.CharFilter(field_name='status')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = LoanExcess
        fields = ['employee', 'loan', 'status', 'created_at']

class LoanExcessViewSet(viewsets.ModelViewSet):
    queryset = LoanExcess.objects.all()
    serializer_class = LoanExcessSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LoanExcessFilter
    search_fields = ['reason']
    ordering_fields = ['amount', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanExcessCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LoanExcessUpdateSerializer
        return LoanExcessSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        excess = self.get_object()
        if excess.status != 'pending':
            return Response(
                {'error': 'Only pending excesses can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        excess.status = 'approved'
        excess.approved_by = request.user
        excess.approved_at = timezone.now()
        excess.save()
        serializer = self.get_serializer(excess)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        excess = self.get_object()
        if excess.status != 'pending':
            return Response(
                {'error': 'Only pending excesses can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        excess.status = 'rejected'
        excess.approved_by = request.user
        excess.approved_at = timezone.now()
        excess.save()
        serializer = self.get_serializer(excess)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_excesses = queryset.count()
        total_amount = queryset.aggregate(total=models.Sum('amount'))['total'] or 0
        pending_count = queryset.filter(status='pending').count()
        approved_count = queryset.filter(status='approved').count()
        rejected_count = queryset.filter(status='rejected').count()

        return Response({
            'total_excesses': total_excesses,
            'total_amount': total_amount,
            'pending_count': pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count
        }) 