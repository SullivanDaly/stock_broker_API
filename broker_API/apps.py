import os
from django.apps import AppConfig

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class BrokerApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'broker_API'

    def ready(self):
        from .db_scripts import start_update_stock_prices_thread
        start_update_stock_prices_thread()  # Start the thread when the app is ready