from django.contrib import admin

from .models import Payment, PaymentMethod


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'tg_user',
                    'status',
                    'paid',
                    'amount',
                    'currency',
                    'description',
                    'created_at',
                    'paid_at',)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass
