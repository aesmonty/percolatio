from django.apps import AppConfig


class FoundationsAppConfig(AppConfig):
    name = 'conduit.apps.foundations'
    label = 'foundations'
    verbose_name = 'Foundations'


default_app_config = 'conduit.apps.foundations.FoundationsAppConfig'
