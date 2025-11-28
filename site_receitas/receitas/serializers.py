from rest_framework import serializers
from receitas.models import Receita


class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Receita."""
    autor_nome = serializers.CharField(source='autor.username', read_only=True)
    foto_da_receita = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        """Meta class para o serializer ReceitaSerializer."""
        model = Receita
        fields = [
            'id', 'autor_nome', 'titulo', 'ingredientes', 'modo_de_preparo',
            'tempo_de_preparo', 'porcoes', 'categoria', 'foto_da_receita',
            'visibilidade', 'autor'
        ]
        read_only_fields = ['autor']

    def to_representation(self, instance):
        """Customiza a representação para retornar URL completa da imagem."""
        data = super().to_representation(instance)

        if instance.foto_da_receita:
            request = self.context.get('request')
            if request is not None:
                data['foto_da_receita'] = request.build_absolute_uri(instance.foto_da_receita.url)
            else:
                data['foto_da_receita'] = instance.foto_da_receita.url

        # Representa a categoria como um objeto com label e value
        try:
            categoria_value = instance.categoria
            categoria_label = instance.get_categoria_display()
            data['categoria'] = {'value': categoria_value, 'label': categoria_label}
        except Exception:
            # se algo der errado, mantenha o valor bruto
            data['categoria'] = getattr(instance, 'categoria', None)

        return data