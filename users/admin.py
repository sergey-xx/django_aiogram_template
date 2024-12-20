from django.contrib import admin

from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'username',
        'birth_date',
        'phone_number',
        'telegram_id',
        'is_admin',
        'created_at',
    )
