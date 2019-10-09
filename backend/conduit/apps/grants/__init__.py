from django.apps import AppConfig


class GrantsAppConfig(AppConfig):
    name = 'conduit.apps.grants'
    label = 'grants'
    verbose_name = 'Grants'

    def ready(self):
        import conduit.apps.grants.signals


default_app_config = 'conduit.apps.grants.GrantsAppConfig'
