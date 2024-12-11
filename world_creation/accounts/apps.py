from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'world_creation.accounts'


# Във файл apps.py на твоето приложение


class AccountsConfig(AppConfig):
    name = 'world_creation.accounts'

    def ready(self):
        import world_creation.accounts.signals  # Импортираме сигналите
