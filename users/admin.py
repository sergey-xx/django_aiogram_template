from django.contrib import admin

from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'first_last_name',
        'username',
        'phone_number',
        'telegram_id',
        'is_admin',
        'created_at',
    )
