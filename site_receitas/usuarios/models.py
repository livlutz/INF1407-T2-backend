from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    """Modelo de usuário personalizado.

    Args:
        AbstractUser (AbstractUser): Classe base para usuários do Django.
    """

    id = models.AutoField(primary_key=True) # Identificador único do usuário

    email = models.EmailField(help_text='Digite seu email', unique=True) # Email do usuário

    foto_de_perfil = models.ImageField(upload_to='usuarios/img', null=True, blank=True) # Foto de perfil do usuário

    class Meta:
        """define o nome do app no admin do django.
        """
        app_label = 'usuarios'

    def __str__(self):
        """Retorna o nome de usuário como representação em string do objeto.

        Returns:
            str: Nome de usuário do usuário.
        """
        return self.username
