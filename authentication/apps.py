from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        import authentication.signals
