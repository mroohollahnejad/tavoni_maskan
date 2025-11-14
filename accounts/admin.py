from django.contrib import admin
from .models import ApprovedPaymentDate

@admin.register(ApprovedPaymentDate)
class ApprovedPaymentDateAdmin(admin.ModelAdmin):
    list_display = ('installment_number', 'due_date')
    list_editable = ('due_date',)
    ordering = ('installment_number',)
