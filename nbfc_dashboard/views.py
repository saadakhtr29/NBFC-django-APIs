from django.db.models import Count, Sum, Avg, F, Q
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import DashboardWidget, SavedReport
from .serializers import (
    DashboardWidgetSerializer, DashboardWidgetCreateSerializer,
    DashboardWidgetUpdateSerializer, SavedReportSerializer,
    SavedReportCreateSerializer, SavedReportUpdateSerializer
)
from nbfc_employees.models import Employee
from nbfc_loans.models import Loan
from nbfc_attendance.models import Attendance
from nbfc_salaries.models import Salary
from nbfc_repayments.models import LoanRepayment
from datetime import datetime, timedelta

class DashboardWidgetFilter(filters.FilterSet):
    organization = filters.NumberFilter(field_name='organization__id')
    widget_type = filters.CharFilter(field_name='widget_type')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = DashboardWidget
        fields = ['organization', 'widget_type', 'is_active']

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = DashboardWidgetFilter
    search_fields = ['name']
    ordering_fields = ['position', 'created_at']
    ordering = ['position']

    def get_serializer_class(self):
        if self.action == 'create':
            return DashboardWidgetCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DashboardWidgetUpdateSerializer
        return DashboardWidgetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(organization=self.request.user.organization) &
                (Q(user=self.request.user) | Q(is_public=True))
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavedReportFilter(filters.FilterSet):
    organization = filters.NumberFilter(field_name='organization__id')
    report_type = filters.CharFilter(field_name='report_type')
    is_public = filters.BooleanFilter(field_name='is_public')

    class Meta:
        model = SavedReport
        fields = ['organization', 'report_type', 'is_public']

class SavedReportViewSet(viewsets.ModelViewSet):
    queryset = SavedReport.objects.all()
    serializer_class = SavedReportSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = SavedReportFilter
    search_fields = ['name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return SavedReportCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SavedReportUpdateSerializer
        return SavedReportSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(organization=self.request.user.organization) &
                (Q(user=self.request.user) | Q(is_public=True))
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        organization = request.user.organization
        today = datetime.now().date()
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)

        # Employee statistics
        employee_stats = {
            'total': Employee.objects.filter(organization=organization).count(),
            'active': Employee.objects.filter(organization=organization, is_active=True).count(),
            'by_department': Employee.objects.filter(organization=organization)
                .values('department__name')
                .annotate(count=Count('id'))
                .order_by('-count')
        }

        # Loan statistics
        loan_stats = {
            'total': Loan.objects.filter(organization=organization).count(),
            'active': Loan.objects.filter(organization=organization, status='active').count(),
            'total_amount': Loan.objects.filter(organization=organization).aggregate(
                total=Sum('amount'))['total'] or 0,
            'monthly_disbursement': Loan.objects.filter(
                organization=organization,
                created_at__gte=month_start
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'by_status': Loan.objects.filter(organization=organization)
                .values('status')
                .annotate(count=Count('id'))
                .order_by('-count')
        }

        # Repayment statistics
        repayment_stats = {
            'total_collected': LoanRepayment.objects.filter(
                organization=organization
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'monthly_collection': LoanRepayment.objects.filter(
                organization=organization,
                created_at__gte=month_start
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'overdue': LoanRepayment.objects.filter(
                organization=organization,
                due_date__lt=today,
                status='pending'
            ).aggregate(total=Sum('amount'))['total'] or 0
        }

        # Attendance statistics
        attendance_stats = {
            'present_today': Attendance.objects.filter(
                organization=organization,
                date=today,
                status='present'
            ).count(),
            'absent_today': Attendance.objects.filter(
                organization=organization,
                date=today,
                status='absent'
            ).count(),
            'monthly_attendance': Attendance.objects.filter(
                organization=organization,
                date__gte=month_start
            ).values('status').annotate(count=Count('id'))
        }

        # Salary statistics
        salary_stats = {
            'total_paid': Salary.objects.filter(
                organization=organization
            ).aggregate(total=Sum('net_salary'))['total'] or 0,
            'monthly_paid': Salary.objects.filter(
                organization=organization,
                month__gte=month_start
            ).aggregate(total=Sum('net_salary'))['total'] or 0,
            'by_department': Salary.objects.filter(
                organization=organization,
                month__gte=month_start
            ).values('employee__department__name').annotate(
                total=Sum('net_salary')
            ).order_by('-total')
        }

        return Response({
            'employee': employee_stats,
            'loan': loan_stats,
            'repayment': repayment_stats,
            'attendance': attendance_stats,
            'salary': salary_stats
        })

    @action(detail=False, methods=['get'])
    def trends(self, request):
        organization = request.user.organization
        today = datetime.now().date()
        year_start = today.replace(month=1, day=1)

        # Monthly loan disbursement trend
        loan_trend = Loan.objects.filter(
            organization=organization,
            created_at__gte=year_start
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            amount=Sum('amount')
        ).order_by('month')

        # Monthly repayment collection trend
        repayment_trend = LoanRepayment.objects.filter(
            organization=organization,
            created_at__gte=year_start
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            amount=Sum('amount')
        ).order_by('month')

        # Monthly attendance trend
        attendance_trend = Attendance.objects.filter(
            organization=organization,
            date__gte=year_start
        ).annotate(
            month=TruncMonth('date')
        ).values('month', 'status').annotate(
            count=Count('id')
        ).order_by('month', 'status')

        # Monthly salary trend
        salary_trend = Salary.objects.filter(
            organization=organization,
            month__gte=year_start
        ).values('month').annotate(
            amount=Sum('net_salary')
        ).order_by('month')

        return Response({
            'loan': loan_trend,
            'repayment': repayment_trend,
            'attendance': attendance_trend,
            'salary': salary_trend
        }) 