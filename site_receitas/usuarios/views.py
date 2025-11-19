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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

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

class PerfilView(APIView):
    """View para exibir o perfil do usuário."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Obter perfil do usuário',
        operation_description='Retorna os detalhes do perfil do usuário especificado.',
        responses={
            200: UsuarioSerializer(),
            404: 'Usuário não encontrado'
        }
    )

    def get(self, request, id, *args, **kwargs):
        """Retorna os detalhes do perfil do usuário."""
        usuario = get_object_or_404(Usuario, id=id)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsuarioUpdateView(APIView):
    """View para atualizar os dados do usuário."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Atualizar dados do usuário',
        operation_description='Atualiza os dados do usuário autenticado.',
        request_body=UsuarioUpdateSerializer,
        responses={
            200: UsuarioSerializer(),
            400: 'Erro de validação',
            401: 'Não autenticado'
        }
    )

    def put(self, request, *args, **kwargs):
        """Atualiza os dados do usuário autenticado."""
        usuario = request.user
        serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UsuarioSerializer(usuario).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioDeleteView(APIView):
    """View para deletar o usuário."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Deletar usuário',
        operation_description='Deleta o usuário autenticado.',
        responses={
            204: 'Usuário deletado com sucesso',
            401: 'Não autenticado'
        }
    )

    def delete(self, request, *args, **kwargs):
        """Deleta o usuário autenticado."""
        usuario = request.user
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReceitasUsuarioView(APIView):
    """View para listar as receitas do usuário."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Listar receitas do usuário',
        operation_description='Retorna todas as receitas criadas pelo usuário autenticado.',
        responses={
            200: ReceitaSerializer(many=True),
            401: 'Não autenticado'
        }
    )

    def get(self, request, *args, **kwargs):
        """Retorna todas as receitas do usuário autenticado."""
        usuario = request.user
        receitas = Receita.objects.filter(autor=usuario)
        serializer = ReceitaSerializer(receitas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
