from django.apps import AppConfig


class MatiereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matiere'
    def ready(self):
        import matiere.signals
