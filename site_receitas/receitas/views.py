from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from receitas.models import Receita
from django.views.generic.base import View
from usuarios.models import Usuario
from receitas.forms import ReceitaModel2Form
from django.urls.base import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ReceitasCreateView(LoginRequiredMixin, View):
    """View que cria uma nova receita.

    Args:
        View (View): um tipo de view baseada em classe
    """

    def get(self, request, *args, **kwargs):
        """Renderiza o formulario para criar uma nova receita.

        Args:
            request (HttpRequest): A requisição HTTP.

        Returns:
            HttpResponse: A resposta HTTP com o formulario de criação de receita.
        """
        contexto = {'formulario': ReceitaModel2Form,
                    'titulo_pagina': 'Criar Receita',
                    'titulo_janela': 'Criar Nova Receita',
                    'botao': 'Criar Receita', }
        return render(request, 'receitas/criarReceita.html', contexto)


    def post(self, request, *args, **kwargs):
        """Processa o formulario para criar uma nova receita.

        Args:
            request (HttpRequest): A requisição HTTP.

        Returns:
            HttpResponse: A resposta HTTP após a criação da receita.
        """
        formulario = ReceitaModel2Form(request.POST, request.FILES)

        if formulario.is_valid():
            receita = formulario.save(commit=False)
            receita.autor = request.user
            receita.save()
            return HttpResponseRedirect(reverse_lazy("receitas:homepage"))

        else:
            contexto = {'formulario': formulario,'mensagem': 'Erro ao criar receita!'}
            return render(request, 'receitas/criarReceita.html', contexto)

class PubReceitasListView(View):
    """View que lista as receitas públicas.

    Args:
        View (View): Classe base para views baseadas em classe.
    """

    def get(self, request, *args, **kwargs):
        """Renderiza a lista de receitas públicas.

        Args:
            request (HttpRequest): A requisição HTTP.

        Returns:
            HttpResponse: A resposta HTTP com a lista de receitas públicas.
        """

        receitas = Receita.objects.filter(visibilidade='pub')

        contexto = {
            'pub_receitas': receitas,
            'titulo_janela': 'Receitas Públicas',
            'titulo_pagina': 'Homepage - Receitas',
        }

        return render(request, 'receitas/home.html', contexto)

class ReceitasUpdateView(LoginRequiredMixin, View):
    """View que atualiza uma receita. Apenas o autor pode editar."""
    login_url = '/login/'  # redireciona se não estiver logado

    def get(self, request, id, *args, **kwargs):
        receita = get_object_or_404(Receita, id=id)

        # Verifica se o usuário é o autor da receita
        if request.user != receita.autor:
            return redirect('receitas:homepage')  # ou página de erro

        formulario = ReceitaModel2Form(instance=receita)

        contexto = {
            'formulario': formulario,
            'titulo_pagina': 'Editar',
            'titulo_janela': 'Editar Receita',
            'botao': 'Salvar',
        }
        return render(request, 'receitas/atualizaReceita.html', contexto)

    def post(self, request, id, *args, **kwargs):
        receita = get_object_or_404(Receita, id=id)

        # Verifica se o usuário é o autor da receita
        if request.user != receita.autor:
            return redirect('receitas:homepage')  # ou página de erro

        formulario = ReceitaModel2Form(request.POST, request.FILES, instance=receita)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy("receitas:homepage"))

        contexto = {
            'formulario': formulario,
            'mensagem': 'Erro ao editar receita!',
            'titulo_pagina': 'Editar',
            'titulo_janela': 'Editar Receita',
            'botao': 'Salvar',
        }
        return render(request, 'receitas/atualizaReceita.html', contexto)

class ReceitasDeleteView(View):
    """View que deleta uma receita.

    Args:
        View (View): Classe base para views baseadas em classe.
    """

    def get(self, request, id, *args, **kwargs):
        """Renderiza a confirmação para deletar a receita.

        Args:
            request (HttpRequest): A requisição HTTP.
            id (int): O ID da receita a ser deletada.

        Returns:
            HttpResponse: A resposta HTTP com a confirmação de deleção da receita.
        """
         # Verifica se o usuário é o autor da receita
        if request.user != receita.autor:
            return redirect('receitas:homepage')  # ou página de erro

        receita = get_object_or_404(Receita, id=id)
        contexto = {'receita': receita,
                    'titulo_pagina': 'Deletar',
                    'titulo_janela': 'Deletar Receita',
                    'botao': 'Deletar', }

        return render(request, 'receitas/deletaReceita.html', contexto)


    def post(self, request, id, *args, **kwargs):
        """Processa a confirmação para deletar a receita.

        Args:
            request (HttpRequest): A requisição HTTP.
            id (int): O ID da receita a ser deletada.

        Returns:
            HttpResponse: A resposta HTTP após a deleção da receita.
        """

        # Verifica se o usuário é o autor da receita
        if request.user != receita.autor:
            return redirect('receitas:homepage')  # ou página de erro

        receita = get_object_or_404(Receita, id=id)

        receita.delete()

        return HttpResponseRedirect(reverse_lazy("receitas:homepage"))

class VerReceita(View):
    """View que exibe os detalhes de uma receita.

    Args:
        View (View): Classe base para views baseadas em classe.
    """

    def get(self, request,id, *args, **kwargs):
        """Renderiza os detalhes da receita.

        Args:
            request (HttpRequest): A requisição HTTP.
            id (int): O ID da receita a ser exibida.

        Returns:
            HttpResponse: A resposta HTTP com os detalhes da receita.
        """
        
        receita = get_object_or_404(Receita, pk=self.kwargs['id'])
        if receita.visibilidade == 'priv' or receita.visibilidade == 'Priv':
            if receita.autor != request.user.id:
                return redirect('receitas:homepage')

        else:
            contexto = { 'receita': receita,
                        'titulo_pagina': 'Ver receita',
                        'titulo_janela': 'Vendo receita',
                }
            return render(request,'receitas/ver_receita.html',contexto)
