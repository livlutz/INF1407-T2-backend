from rest_framework import serializers
from usuarios.models import Usuario
from rest_framework.authtoken.models import Token


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para visualização de usuário."""
    foto_de_perfil = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'foto_de_perfil', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def to_representation(self, instance):
        """Customiza a representação para retornar URL completa da foto de perfil."""
        data = super().to_representation(instance)

        if instance.foto_de_perfil:
            request = self.context.get('request')
            if request is not None:
                data['foto_de_perfil'] = request.build_absolute_uri(instance.foto_de_perfil.url)
            else:
                data['foto_de_perfil'] = instance.foto_de_perfil.url

        return data


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário."""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        """Meta class para o serializer de criação de usuário."""
        model = Usuario
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'foto_de_perfil']

    def validate(self, data):
        """Valida se as senhas coincidem."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'As senhas não coincidem.'})
        return data

    def create(self, validated_data):
        """Cria um novo usuário e gera um token de autenticação."""
        validated_data.pop('password_confirm')
        user = Usuario.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de usuário."""
    foto_de_perfil = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'foto_de_perfil']

    def to_representation(self, instance):
        """Customiza a representação para retornar URL completa da foto de perfil."""
        data = super().to_representation(instance)

        if instance.foto_de_perfil:
            request = self.context.get('request')
            if request is not None:
                data['foto_de_perfil'] = request.build_absolute_uri(instance.foto_de_perfil.url)
            else:
                data['foto_de_perfil'] = instance.foto_de_perfil.url

        return data