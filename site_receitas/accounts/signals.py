from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Handles password reset tokens
    Gera os tokens de reset de senha
    Token é criado e pode ser recuperado via API para exibição no frontend
    :param sender: Classe View que manda o sinal
    :param instance: Instância da View que mandou o sinal
    :param reset_password_token: Objeto do Modelo Token
    :param args:
    :param kwargs:
    :return:
    """
    # Token é criado automicamente pelo django_rest_passwordreset
    # Frontend irá exibir as informações de reset ao invés de enviar email
    pass