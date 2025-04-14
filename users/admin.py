from django.contrib import admin

from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'username',
        'phone_number',
        'tg_id',
        'is_admin',
        'created_at',
    )
