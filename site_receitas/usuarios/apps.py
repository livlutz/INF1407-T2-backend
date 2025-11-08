from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    """Configuração da aplicação de usuários.

    Args:
        AppConfig (_type_): classe base para configuração de aplicativos Django
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"
