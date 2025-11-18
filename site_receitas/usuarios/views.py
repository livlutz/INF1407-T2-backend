from django.shortcuts import get_object_or_404
from usuarios.models import Usuario
from receitas.models import Receita
from usuarios.serializers import UsuarioSerializer, UsuarioCreateSerializer, UsuarioUpdateSerializer
from receitas.serializers import ReceitaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authtoken.models import Token


# Create your views here.

class UsuarioLoginView(APIView):
    """View de login do usuário."""

    @swagger_auto_schema(
        operation_summary='Informações sobre login',
        operation_description='Retorna informações sobre como fazer login. O token de autenticação será retornado ao fazer login com sucesso.',
        responses={
            200: openapi.Response(
                description='Informações de login',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'instructions': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        }
    )

    def get(self, request, *args, **kwargs):
        """Retorna informações sobre o login."""
        return Response({
            'message': 'Faça login para obter um token de autenticação.',
            'instructions': 'Use seu username e senha para fazer login. O token será retornado na resposta.',
            'required_fields': ['username', 'password']
        }, status=status.HTTP_200_OK)

class UsuarioCreateView(APIView):
    """View de criação de usuário."""

    @swagger_auto_schema(
        operation_summary='Criar novo usuário',
        operation_description='Cria um novo usuário no sistema.',
        request_body=UsuarioCreateSerializer,
        responses={
            201: UsuarioSerializer(),
            400: 'Erro de validação'
        }
    )

    def post(self, request, *args, **kwargs):
        """Cria um novo usuário."""
        serializer = UsuarioCreateSerializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()
            token, _ = Token.objects.get_or_create(user=usuario)
            return Response({
                'user': UsuarioSerializer(usuario).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
