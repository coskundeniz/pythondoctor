from django.apps import AppConfig


class PdMainConfig(AppConfig):
    name = 'pd_main'

    def ready(self):
        import pd_main.signals