from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import Document
from .serializers import (
    DocumentSerializer, DocumentCreateSerializer, DocumentUpdateSerializer
)
from django.utils import timezone

# Create your views here.

class DocumentFilter(filters.FilterSet):
    loan = filters.NumberFilter(field_name='loan__id')
    document_type = filters.CharFilter(field_name='document_type')
    status = filters.CharFilter(field_name='status')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = Document
        fields = ['loan', 'document_type', 'status', 'created_at']

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = DocumentFilter
    search_fields = ['loan__employee__first_name', 'loan__employee__last_name', 'description']
    ordering_fields = ['document_type', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DocumentUpdateSerializer
        return DocumentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(loan__organization=self.request.user.organization)
        return queryset

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        document = self.get_object()
        document.status = 'verified'
        document.verified_by = request.user
        document.verified_at = timezone.now()
        document.save()
        return Response(DocumentSerializer(document).data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_documents = queryset.count()
        verified = queryset.filter(status='verified').count()
        pending = queryset.filter(status='pending').count()
        rejected = queryset.filter(status='rejected').count()
        return Response({
            'total_documents': total_documents,
            'verified': verified,
            'pending': pending,
            'rejected': rejected
        })
