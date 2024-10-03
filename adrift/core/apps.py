from django.apps import AppConfig
from core.kafka import close_producer
import atexit

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # this will automatically register the signal
        from .signals import log_save, log_delete

        atexit.register(close_producer)