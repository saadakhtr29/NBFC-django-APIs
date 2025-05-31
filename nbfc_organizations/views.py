from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Organization, Department

from .serializers import (
    OrganizationSerializer,
    OrganizationCreateSerializer,
    OrganizationUpdateSerializer,
    ChangeOrganizationPasswordSerializer,
    DepartmentSerializer
)

User = get_user_model()

class OrganizationFilter(filters.FilterSet):
    class Meta:
        model = Organization
        fields = {
            'name': ['exact', 'icontains'],
            'code': ['exact'],
            'is_active': ['exact'],
            'created_at': ['gte', 'lte'],
        }

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = OrganizationFilter
    search_fields = ['name', 'code', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrganizationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrganizationUpdateSerializer
        return OrganizationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        organization = self.get_object()
        return Response({
            'total_employees': organization.total_employees,
            'total_loans': organization.total_loans,
            'total_loan_amount': organization.total_loan_amount,
            'total_repayment_amount': organization.total_repayment_amount,
        })

class OrganizationListView(generics.ListAPIView):
    """View for listing organizations."""
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['type', 'industry', 'status']
    search_fields = ['name', 'code', 'city', 'state', 'country']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Organization.objects.all()
        return Organization.objects.filter(user=user)

class OrganizationDetailView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating organization details."""
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Organization.objects.all()
        return Organization.objects.filter(user=user)

class OrganizationUpdateView(generics.UpdateAPIView):
    """View for updating organization information."""
    queryset = Organization.objects.all()
    serializer_class = OrganizationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Organization.objects.all()
        return Organization.objects.filter(user=user)

class ChangeOrganizationPasswordView(APIView):
    """View for changing organization password."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        if not request.user.is_staff and organization.user != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ChangeOrganizationPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = organization.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"detail": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password successfully updated."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['organization', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_admin:
            return queryset.filter(organization=self.request.user.organization)
        return queryset

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        department = self.get_object()
        return Response({
            'total_employees': department.total_employees,
        })
