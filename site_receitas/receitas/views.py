from django.shortcuts import get_object_or_404
from receitas.models import Receita
from django.db.models import Q
from receitas.serializers import ReceitaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from drf_yasg import openapi


class ReceitasCreateView(APIView):
    """View que cria uma nova receita."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Criar nova receita',
        operation_description='Cria uma nova receita. Requer autenticação.',
        request_body=ReceitaSerializer,
        responses={
            201: ReceitaSerializer,
            400: 'Erro de validação',
            401: 'Não autenticado'
        }
    )
    def post(self, request, *args, **kwargs):
        """Processa o formulário para criar uma nova receita."""
        serializer = ReceitaSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(autor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisibleReceitasListView(APIView):
    """View que lista as receitas visíveis para o usuário."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Lista todas as receitas visíveis para o usuário',
        operation_description='Mostra as receitas que têm visibilidade pública e, se o usuário estiver autenticado, também as receitas privadas dele.',
        responses={
            200: ReceitaSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        """Retorna a lista de receitas públicas."""
        usuario = request.user

        if request.user.is_authenticated:
            receitas = Receita.objects.filter(Q(visibilidade='pub') | Q(autor=usuario)).order_by('-id')
        else:
            receitas = Receita.objects.filter(visibilidade='pub').order_by('-id')

        serializer = ReceitaSerializer(receitas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceitasUpdateView(APIView):
    """View que atualiza uma receita. Apenas o autor pode editar."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Atualiza uma receita',
        operation_description='Atualiza uma receita existente e requer autenticação, apenas o autor da receita pode editá-la.',
        request_body=ReceitaSerializer,
        responses={
            200: ReceitaSerializer,
            400: 'Erro de validação',
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Receita não encontrada'
        }
    )
    def put(self, request, id, *args, **kwargs):
        """Atualiza uma receita."""
        receita = get_object_or_404(Receita, id=id)

        if request.user != receita.autor:
            return Response(
                {'error': 'Você não tem permissão para editar esta receita.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ReceitaSerializer(receita, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceitasDeleteView(APIView):
    """View que deleta uma receita."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Deletar uma receita',
        operation_description='Deleta uma receita existente. Requer autenticação, apenas o autor da receita pode deletá-la.',
        responses={
            200: openapi.Response(
                description='Receita deletada com sucesso',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Receita não encontrada'
        }
    )
    def delete(self, request, id, *args, **kwargs):
        """Deleta uma receita."""
        receita = get_object_or_404(Receita, id=id)

        if request.user != receita.autor:
            return Response(
                {'error': 'Você não tem permissão para deletar esta receita.'},
                status=status.HTTP_403_FORBIDDEN
            )

        receita.delete()
        return Response(
            {'message': 'Receita deletada com sucesso.'},
            status=status.HTTP_200_OK
        )


class VerReceita(APIView):
    """View que exibe os detalhes de uma receita."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Ver detalhes de uma receita',
        operation_description='Retorna os detalhes de uma receita específica. Receitas privadas só podem ser visualizadas pelo autor.',
        responses={
            200: ReceitaSerializer,
            403: 'Esta receita é privada e você não tem permissão para visualizá-la.',
            404: 'Receita não encontrada'
        }
    )
    def get(self, request, id, *args, **kwargs):
        """Retorna os detalhes da receita."""
        receita = get_object_or_404(Receita, pk=id)

        if receita.visibilidade in ['priv', 'Priv']:
            if not request.user.is_authenticated or receita.autor != request.user:
                return Response(
                    {'error': 'Você não tem permissão para visualizar esta receita.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = ReceitaSerializer(receita, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)