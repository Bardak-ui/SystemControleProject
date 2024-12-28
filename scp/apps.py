from django.apps import AppConfig


class ScpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scp'

    def ready(self):
        import scp.signals
