from django.apps import AppConfig


class RecipesiteConfig(AppConfig):
    name = 'recipeSite'

    def ready(self):
        import users.signals