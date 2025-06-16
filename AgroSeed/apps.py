from django.apps import AppConfig



class AgroseedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AgroSeed'

    def ready(self):
        import AgroSeed.signals