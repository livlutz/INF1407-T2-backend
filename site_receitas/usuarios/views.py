from django.shortcuts import get_object_or_404
from usuarios.models import Usuario
from receitas.models import Receita
from usuarios.serializers import UsuarioSerializer, UsuarioCreateSerializer, UsuarioUpdateSerializer, ReceitaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class UsuarioLoginView(APIView):
    """View de login do usuário."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Login de usuário',
        operation_description='Realiza login e retorna token de autenticação.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description='Login realizado com sucesso',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': UsuarioSerializer,
                    }
                )
            ),
            400: 'Credenciais inválidas',
        }
    )
    def post(self, request, *args, **kwargs):
        """Realiza o login do usuário."""
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UsuarioSerializer(user)
            return Response({
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Credenciais inválidas'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsuarioLogoutView(APIView):
    """View de logout do usuário."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Logout de usuário',
        operation_description='Realiza logout e deleta o token de autenticação.',
        responses={
            200: 'Logout realizado com sucesso',
            401: 'Não autenticado'
        }
    )
    def post(self, request, *args, **kwargs):
        """Realiza o logout do usuário."""
        request.user.auth_token.delete()
        return Response(
            {'message': 'Logout realizado com sucesso'},
            status=status.HTTP_200_OK
        )


class PerfilView(APIView):
    """View de visualizar perfil do usuário."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Ver perfil do usuário',
        operation_description='Retorna os dados do perfil do usuário. Apenas o próprio usuário pode visualizar.',
        responses={
            200: UsuarioSerializer,
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Usuário não encontrado'
        }
    )
    def get(self, request, id, *args, **kwargs):
        """Retorna o perfil do usuário."""
        if request.user.id != int(id):
            return Response(
                {'error': 'Você não tem permissão para visualizar este perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )

        usuario = get_object_or_404(Usuario, pk=id)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsuarioCreateView(APIView):
    """View de criação de usuário."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Criar novo usuário',
        operation_description='Cria um novo usuário no sistema.',
        request_body=UsuarioCreateSerializer,
        responses={
            201: UsuarioSerializer,
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


class UsuarioUpdateView(APIView):
    """View de atualização de usuário."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Atualizar dados do usuário',
        operation_description='Atualiza os dados do usuário. Apenas o próprio usuário pode atualizar.',
        request_body=UsuarioUpdateSerializer,
        responses={
            200: UsuarioSerializer,
            400: 'Erro de validação',
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Usuário não encontrado'
        }
    )
    def put(self, request, id, *args, **kwargs):
        """Atualiza os dados do usuário."""
        if request.user.id != int(id):
            return Response(
                {'error': 'Você não tem permissão para atualizar este perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )

        usuario = get_object_or_404(Usuario, pk=id)
        serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(UsuarioSerializer(usuario).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDeleteView(APIView):
    """View de deletar usuário."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Deletar usuário',
        operation_description='Deleta a conta do usuário. Apenas o próprio usuário pode deletar.',
        responses={
            204: 'Usuário deletado com sucesso',
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Usuário não encontrado'
        }
    )
    def delete(self, request, id, *args, **kwargs):
        """Deleta o usuário."""
        if request.user.id != int(id):
            return Response(
                {'error': 'Você não tem permissão para deletar este perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )

        usuario = get_object_or_404(Usuario, pk=id)
        usuario.delete()
        return Response(
            {'message': 'Usuário deletado com sucesso.'},
            status=status.HTTP_204_NO_CONTENT
        )


class ReceitasUsuarioView(APIView):
    """View de listar receitas do usuário."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Listar receitas do usuário',
        operation_description='Retorna todas as receitas criadas pelo usuário. Apenas o próprio usuário pode visualizar.',
        responses={
            200: ReceitaSerializer(many=True),
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Usuário não encontrado'
        }
    )
    def get(self, request, id, *args, **kwargs):
        """Retorna as receitas do usuário."""
        if request.user.id != int(id):
            return Response(
                {'error': 'Você não tem permissão para visualizar estas receitas.'},
                status=status.HTTP_403_FORBIDDEN
            )

        usuario = get_object_or_404(Usuario, pk=id)
        receitas = Receita.objects.filter(autor=usuario).order_by('-id')
        serializer = ReceitaSerializer(receitas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    """View para alteração de senha."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Alterar senha',
        operation_description='Altera a senha do usuário autenticado.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: 'Senha alterada com sucesso',
            400: 'Senha antiga incorreta ou senha nova inválida',
            401: 'Não autenticado'
        }
    )
    def post(self, request, *args, **kwargs):
        """Altera a senha do usuário."""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not request.user.check_password(old_password):
            return Response(
                {'error': 'Senha antiga incorreta.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {'message': 'Senha alterada com sucesso.'},
            status=status.HTTP_200_OK
        )