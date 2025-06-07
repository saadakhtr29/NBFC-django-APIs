from django.db import models
from django.utils.translation import gettext_lazy as _
from nbfc_employees.models import Employee
from nbfc_accounts.models import User

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nbfc_attendance'
        ordering = ['-date', '-check_in']
        unique_together = ['employee', 'date']
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendance Records')

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date} - {self.status}"

    @property
    def is_verified(self):
        return self.verified_at is not None

    @property
    def is_late(self):
        if self.check_in:
            # Assuming work starts at 9:00 AM
            return self.check_in > models.time(9, 0)
        return False

    @property
    def is_early_leave(self):
        if self.check_out:
            # Assuming work ends at 5:00 PM
            return self.check_out < models.time(17, 0)
        return False
