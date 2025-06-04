from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the 'users' application.
    Sets the default primary key field type and app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        pass
