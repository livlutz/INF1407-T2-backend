from django.shortcuts import get_object_or_404, redirect
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

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
        serializer = ReceitaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(autor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PubReceitasListView(APIView):
    """View que lista as receitas públicas."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Lista todas as receitas públicas',
        operation_description='Mostra as receitas que têm visibilidade pública e não requer login.',
        responses={
            200: ReceitaSerializer(many=True),
        }
    )

    def get(self, request, *args, **kwargs):
        """Retorna a lista de receitas públicas."""
        receitas = Receita.objects.filter(visibilidade='pub').order_by('-id')
        serializer = ReceitaSerializer(receitas, many=True)
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

        # Verifica se o usuário é o autor da receita
        if request.user != receita.autor:
            return Response(
                {'error': 'Você não tem permissão para editar esta receita.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ReceitaSerializer(receita, data=request.data, partial=True)

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
            204: 'Receita deletada com sucesso',
            401: 'Não autenticado',
            403: 'Sem permissão',
            404: 'Receita não encontrada'
        }
    )#
    def delete(self, request, id, *args, **kwargs):
        """Deleta uma receita."""
        receita = get_object_or_404(Receita, id=id)

        # Verifica se o usuário é o autor da receita
        if request.user != receita.autor:
            return Response(
                {'error': 'Você não tem permissão para deletar esta receita.'},
                status=status.HTTP_403_FORBIDDEN
            )

        receita.delete()
        return Response(
            {'message': 'Receita deletada com sucesso.'},
            status=status.HTTP_204_NO_CONTENT
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

        serializer = ReceitaSerializer(receita)
        return Response(serializer.data, status=status.HTTP_200_OK)