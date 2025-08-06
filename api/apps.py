from django.apps import AppConfig

class MyappConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals