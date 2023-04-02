from django.apps import AppConfig
from django.db.models.signals import post_migrate


def generate_data(*args, **kwargs):
    from .factories import generate_mock_data
    from .models import Book

    if Book.objects.count() == 0:
        print("Importing some mock data")
        generate_mock_data()


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self) -> None:
        post_migrate.connect(lambda *args, **kwargs: generate_data(), sender=self)
