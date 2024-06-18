from django.apps import AppConfig


class LiveconfigsConfig(AppConfig):
    name = 'liveconfigs'

    def ready(self) -> None:
        import liveconfigs.config
