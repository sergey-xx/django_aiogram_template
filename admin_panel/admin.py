from django.contrib import admin

from admin_panel.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    pass
