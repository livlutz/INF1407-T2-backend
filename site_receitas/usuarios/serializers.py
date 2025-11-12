from rest_framework import serializers
from usuarios.models import Usuario
from receitas.models import Receita


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para visualização de usuário."""

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'foto', 'data_nascimento', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'foto', 'data_nascimento']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de usuário."""

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'foto', 'data_nascimento']


class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para receitas (usado na listagem de receitas do usuário)."""
    autor_nome = serializers.CharField(source='autor.username', read_only=True)

    class Meta:
        model = Receita
        fields = '__all__'
        read_only_fields = ['autor', 'id']