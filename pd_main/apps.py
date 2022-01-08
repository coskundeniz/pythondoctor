from django.apps import AppConfig


class PdMainConfig(AppConfig):
    name = 'pd_main'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        import pd_main.signals
