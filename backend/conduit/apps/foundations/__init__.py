from django.apps import AppConfig


class FoundationsAppConfig(AppConfig):
    name = 'conduit.apps.foundations'
    label = 'foundations'
    verbose_name = 'Foundations'

    def ready(self):
        import conduit.apps.foundations.signals

default_app_config = 'conduit.apps.foundations.FoundationsAppConfig'
