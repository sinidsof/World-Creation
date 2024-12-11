from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'world_creation.tasks'


from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'world_creation.accounts'

    def ready(self):
        import world_creation.accounts.signals
