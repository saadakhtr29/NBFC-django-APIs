from django.contrib import admin
from .models import Repayment

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('loan__employee__first_name', 'loan__employee__last_name')
    ordering = ('-payment_date',)
