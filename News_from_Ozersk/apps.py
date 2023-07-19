from django.apps import AppConfig


class NewsFromOzerskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News_from_Ozersk'

    def ready(self):
        import News_from_Ozersk.signals
