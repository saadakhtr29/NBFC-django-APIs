import pandas as pd
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
from .models import BulkUpload
from .serializers import BulkUploadSerializer, BulkUploadCreateSerializer
from nbfc_employees.models import Employee
from nbfc_loans.models import Loan
from nbfc_attendance.models import Attendance
from nbfc_salaries.models import Salary

class BulkUploadFilter(filters.FilterSet):
    organization = filters.NumberFilter(field_name='organization__id')
    upload_type = filters.CharFilter(field_name='upload_type')
    status = filters.CharFilter(field_name='status')
    created_at = filters.DateTimeFilter(field_name='created_at')

    class Meta:
        model = BulkUpload
        fields = ['organization', 'upload_type', 'status', 'created_at']

class BulkUploadViewSet(viewsets.ModelViewSet):
    queryset = BulkUpload.objects.all()
    serializer_class = BulkUploadSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BulkUploadFilter
    search_fields = ['upload_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return BulkUploadCreateSerializer
        return BulkUploadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    def perform_create(self, serializer):
        upload = serializer.save(created_by=self.request.user)
        self.process_upload(upload)

    def process_upload(self, upload):
        try:
            upload.status = 'processing'
            upload.save()

            # Read the Excel file
            file_path = upload.file.path
            df = pd.read_excel(file_path)
            upload.total_records = len(df)
            upload.save()

            success_count = 0
            failure_count = 0
            error_log = []

            if upload.upload_type == 'employees':
                for index, row in df.iterrows():
                    try:
                        Employee.objects.create(
                            organization=upload.organization,
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            email=row['email'],
                            phone=row['phone'],
                            gender=row['gender'],
                            date_of_birth=row['date_of_birth'],
                            joining_date=row['joining_date'],
                            department_id=row['department_id']
                        )
                        success_count += 1
                    except Exception as e:
                        failure_count += 1
                        error_log.append(f"Row {index + 2}: {str(e)}")

            elif upload.upload_type == 'loans':
                for index, row in df.iterrows():
                    try:
                        Loan.objects.create(
                            organization=upload.organization,
                            employee_id=row['employee_id'],
                            amount=row['amount'],
                            interest_rate=row['interest_rate'],
                            term_months=row['term_months'],
                            start_date=row['start_date'],
                            purpose=row['purpose']
                        )
                        success_count += 1
                    except Exception as e:
                        failure_count += 1
                        error_log.append(f"Row {index + 2}: {str(e)}")

            elif upload.upload_type == 'attendance':
                for index, row in df.iterrows():
                    try:
                        Attendance.objects.create(
                            organization=upload.organization,
                            employee_id=row['employee_id'],
                            date=row['date'],
                            status=row['status'],
                            check_in=row.get('check_in'),
                            check_out=row.get('check_out'),
                            working_hours=row.get('working_hours'),
                            notes=row.get('notes')
                        )
                        success_count += 1
                    except Exception as e:
                        failure_count += 1
                        error_log.append(f"Row {index + 2}: {str(e)}")

            elif upload.upload_type == 'salaries':
                for index, row in df.iterrows():
                    try:
                        Salary.objects.create(
                            organization=upload.organization,
                            employee_id=row['employee_id'],
                            month=row['month'],
                            basic_salary=row['basic_salary'],
                            allowances=row.get('allowances', {}),
                            deductions=row.get('deductions', {}),
                            bonus=row.get('bonus', 0),
                            overtime=row.get('overtime', 0),
                            notes=row.get('notes')
                        )
                        success_count += 1
                    except Exception as e:
                        failure_count += 1
                        error_log.append(f"Row {index + 2}: {str(e)}")

            upload.processed_records = len(df)
            upload.success_count = success_count
            upload.failure_count = failure_count
            upload.error_log = json.dumps(error_log)
            upload.status = 'completed' if failure_count == 0 else 'failed'
            upload.save()

        except Exception as e:
            upload.status = 'failed'
            upload.error_log = str(e)
            upload.save()

    @action(detail=False, methods=['get'])
    def download_template(self, request):
        upload_type = request.query_params.get('type')
        if not upload_type:
            return Response(
                {'error': 'Upload type is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Define template columns based on upload type
        if upload_type == 'employees':
            columns = [
                'first_name', 'last_name', 'email', 'phone', 'gender',
                'date_of_birth', 'joining_date', 'department_id'
            ]
        elif upload_type == 'loans':
            columns = [
                'employee_id', 'amount', 'interest_rate', 'term_months',
                'start_date', 'purpose'
            ]
        elif upload_type == 'attendance':
            columns = [
                'employee_id', 'date', 'status', 'check_in', 'check_out',
                'working_hours', 'notes'
            ]
        elif upload_type == 'salaries':
            columns = [
                'employee_id', 'month', 'basic_salary', 'allowances',
                'deductions', 'bonus', 'overtime', 'notes'
            ]
        else:
            return Response(
                {'error': 'Invalid upload type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create template DataFrame
        df = pd.DataFrame(columns=columns)
        
        # Save to temporary file
        template_path = os.path.join(settings.MEDIA_ROOT, 'templates', f'{upload_type}_template.xlsx')
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        df.to_excel(template_path, index=False)

        # Return file
        with open(template_path, 'rb') as f:
            response = Response(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{upload_type}_template.xlsx"'
            return response 