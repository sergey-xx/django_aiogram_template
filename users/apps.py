from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = 'Пользователи Телеграм'

    def ready(self) -> None:
        from backend import config
        return super().ready()
