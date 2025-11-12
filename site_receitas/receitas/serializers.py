from rest_framework import serializers
from receitas.models import Receita

class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para receitas."""
    autor_nome = serializers.CharField(source='autor.username', read_only=True)

    class Meta:
        model = Receita
        fields = '__all__'
        read_only_fields = ['autor', 'id']