from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# Autenticação
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
# Password Reset
from django_rest_passwordreset.models import ResetPasswordToken
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    '''
    View para gerenciamento de tokens de autenticação

    Args:
        ObtainAuthToken (ObtainAuthToken): View padrão do DRF para obtenção de tokens
    '''

    @swagger_auto_schema(
        operation_summary='Obter o token de autenticação',
        operation_description='Retorna o token em caso de sucesso na autenticação ou HTTP 401',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required = ['username', 'password', ],
        ),
        responses={
            status.HTTP_200_OK: 'Token is returned.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
        },
    )

    def post(self, request, *args, **kwargs):
        '''
        Args:
            request (Request): Requisição HTTP com username e password
        Retorna:
            Response: Resposta HTTP com o token ou erro de autenticação
        '''
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Obtém o username do usuário',
        operation_description="Retorna o username e ID do usuário ou apenas visitante se o usuário não estiver autenticado",
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
                default='token ',
            ),
        ],
        responses={
            200: openapi.Response(
                description='Dados do usuário',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )

    def get(self, request):
        '''
        Args:
            request (Request): Requisição HTTP com token de autenticação
        Retorna:
            Response: Resposta HTTP com username e ID do usuário ou visitante
        '''
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
            token_obj = Token.objects.get(key=token)
            user = token_obj.user

            return Response({
                'username': user.username,
                'id': user.id,
                'email': user.email,
            }, status=status.HTTP_200_OK)

        except (Token.DoesNotExist, AttributeError):

            return Response({'username': 'visitante', 'id': None}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Realiza logout do usuário, apagando o seu token',
        operation_summary='Realiza logout',
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING, default='token ',
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
            ),
        ],
        request_body=None,
        responses={
            status.HTTP_200_OK: 'User logged out',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated',
            status.HTTP_403_FORBIDDEN: 'User not authorized to logout',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Erro no servidor',
        },
    )

    def delete(self, request):
        '''
        Args:
            request (Request): Requisição HTTP com token de autenticação
        Retorna:
            Response: Resposta HTTP indicando sucesso ou falha no logout
        '''
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            token_obj = Token.objects.get(key=token)

        except (Token.DoesNotExist, IndexError):
            return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST)

        user = token_obj.user

        if user.is_authenticated:
            request.user = user
            logout(request)

            token = Token.objects.get(user=user)
            token.delete()

            return Response({'msg': 'Logout bem-sucedido.'}, status=status.HTTP_200_OK)

        else:
            return Response({'msg': 'Usuário não autenticado.'}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_description='Troca a senha do usuário, atualiza o token em caso de sucesso',
        operation_summary='Troca a senha do usuário',
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
                default='token ',
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['old_password', 'new_password1', 'new_password2'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Senha alterada com sucesso.",
                examples={ "application/json": { "message": "Senha alterada com sucesso." } }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erro na solicitação.",
                examples={ "application/json": { "old_password": ["Senha atual incorreta."] } }
            ),
        }
    )

    def put(self, request):
        '''
        Args:
            request (Request): Requisição HTTP com token de autenticação e senhas
        Retorna:
            Response: Resposta HTTP indicando sucesso ou falha na troca de senha
        '''
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        oldPassword = request.data.get('old_password')
        newPassword = request.data.get('new_password1')
        confirmPassword = request.data.get('new_password2')

        if newPassword != confirmPassword:
            return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se a senha atual está correta
        if user.check_password(oldPassword):
            # Alterar a senha e atualizar o token
            user.set_password(newPassword)
            user.save()
            # Atualizar token
            try:
                token = Token.objects.get(user=user)
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)

            except Token.DoesNotExist:
                pass
            return Response({'token': token.key, "message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)

        else:
            return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetView(APIView):
    '''
    View personalizada para reset de senha que retorna o token no response
    para ser exibido no frontend
    '''

    @swagger_auto_schema(
        operation_summary='Solicitar reset de senha',
        operation_description='Gera um token de reset de senha e retorna no response para exibição no frontend',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            },
            required=['email'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Token gerado com sucesso',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: 'Email inválido',
        },
    )
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

            # Remove tokens antigos do usuário
            ResetPasswordToken.objects.filter(user=user).delete()

            # Cria novo token
            token = ResetPasswordToken.objects.create(user=user)

            return Response({
                'status': 'OK',
                'token': token.key,
                'message': 'Token de reset gerado com sucesso'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # Por segurança, retorna OK mesmo se usuário não existir
            # Retorna estrutura consistente com campo token vazio
            return Response({
                'status': 'OK',
                'token': None,
                'message': 'Se o email existir, um token foi gerado'
            }, status=status.HTTP_200_OK)


class CustomPasswordResetConfirmView(APIView):
    '''
    View personalizada para confirmar reset de senha
    Requer apenas token e nova senha (não precisa de email)
    '''

    @swagger_auto_schema(
        operation_summary='Confirmar reset de senha',
        operation_description='Confirma o reset de senha usando o token e define nova senha',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['token', 'password'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Senha alterada com sucesso',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: 'Token inválido ou expirado',
        },
    )
    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')

        if not token or not password:
            return Response({
                'status': 'error',
                'message': 'Token e senha são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_token = ResetPasswordToken.objects.get(key=token)

            # Define a nova senha
            user = reset_token.user
            user.set_password(password)
            user.save()

            # Remove o token após uso
            reset_token.delete()

            return Response({
                'status': 'OK',
                'message': 'Senha alterada com sucesso'
            }, status=status.HTTP_200_OK)

        except ResetPasswordToken.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Token inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erro ao processar requisição: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
