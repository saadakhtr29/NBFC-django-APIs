from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from nbfc_django.base_views import BaseModelViewSet
from .models import Attendance
from .serializers import (
    AttendanceSerializer, AttendanceCreateSerializer, AttendanceUpdateSerializer
)
from django.utils import timezone

# Create your views here.

class AttendanceFilter(filters.FilterSet):
    employee = filters.NumberFilter(field_name='employee__id')
    date = filters.DateFilter(field_name='date')
    status = filters.CharFilter(field_name='status')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'created_at']

class AttendanceViewSet(BaseModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = AttendanceFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'notes']
    ordering_fields = ['date', 'check_in', 'created_at']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.action == 'create':
            return AttendanceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AttendanceUpdateSerializer
        return AttendanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__organization=self.request.user.organization)
        return queryset

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        attendance = self.get_object()
        attendance.verified_by = request.user
        attendance.verified_at = timezone.now()
        attendance.save()
        return Response(AttendanceSerializer(attendance).data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        total_attendance = queryset.count()
        present = queryset.filter(status='present').count()
        absent = queryset.filter(status='absent').count()
        late = queryset.filter(status='late').count()
        half_day = queryset.filter(status='half_day').count()
        leave = queryset.filter(status='leave').count()
        return Response({
            'total_attendance': total_attendance,
            'present': present,
            'absent': absent,
            'late': late,
            'half_day': half_day,
            'leave': leave
        })
