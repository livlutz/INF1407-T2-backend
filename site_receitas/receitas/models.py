from django.db import models
from usuarios.models import Usuario
from site_receitas import settings
# Create your models here.

class Receita(models.Model):
    """Modelo que representa uma receita.

    Args:
        models (Models): Classe base para todos os modelos do Django.

    Returns:
        _type_: Retorna uma instância do modelo Receita.
    """

    id = models.AutoField(primary_key=True) # Identificador da receita (primary key)

    titulo = models.CharField(max_length=200, help_text='Digite o titulo da receita') # Título da receita

    ingredientes = models.TextField(help_text='Liste os ingredientes') # Ingredientes da receita

    modo_de_preparo = models.TextField(help_text='Descreva o modo de preparo') # Modo de preparo da receita

    tempo_de_preparo = models.IntegerField(help_text='Tempo de preparo em minutos') # Tempo de preparo da receita

    porcoes = models.IntegerField(help_text='Numero de porcoes/ Quantas pessoas serve') # Porções da receita

    categoria = models.CharField(max_length=100, help_text='Categoria da receita (ex: sobremesa, prato principal, etc.)') # Categoria da receita

    foto_da_receita = models.ImageField(upload_to='receitas/img', null=True, blank=True) # Foto da receita

    # visibilidade da receita (pública ou privada)
    visibilidade = models.CharField(max_length=10, choices=[('pub', 'Pub'), ('priv', 'Priv')], default='Pub', help_text='Defina se a receita é pública ou privada (Pub ou Priv)')

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Autor da receita (chave estrangeira para o modelo Usuario)

    class Meta:
        """define o nome do app para o modelo
        """
        app_label = 'receitas'

    def __str__(self):
        """Retorna o título da receita.

        Returns:
            str: Título da receita.
        """
        return self.titulo

    def tempo_de_preparo_formatado(self):
        """Formata o tempo de preparo para horas e minutos.

        Returns:
            str: Tempo de preparo formatado.
        """

        horas = self.tempo_de_preparo // 60


        minutos = self.tempo_de_preparo % 60

        partes = []

        if horas > 0:
            partes.append(f"{horas} hora{'s' if horas > 1 else ''}")

        if minutos > 0 or horas == 0:
            partes.append(f"{minutos} minuto{'s' if minutos != 1 else ''}")

        return " e ".join(partes)