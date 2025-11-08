
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from usuarios.forms import CustomUserCreationForm, UsuarioLoginForm, UsuarioUpdateForm
from usuarios.models import Usuario
from receitas.models import Receita
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

@login_required
def logout_confirm(request):
    """Função de confirmar logout

    Args:
        request (HttpRequest): A solicitação HTTP recebida.

    Returns:
        _type_: A resposta HTTP com a página de confirmação de logout.
    """
    return render(request, 'usuarios/logout.html')

@login_required
def perfil(request, id):
    """Função de mostrar o perfil do usuario logado

    Args:
        request (HttpRequest): A solicitação HTTP recebida.
        id (int): id do usuario logado.

    Returns:
        HttpResponse: A resposta HTTP com a página de perfil do usuário.
    """
    # Garante que o usuário está autenticado e é o dono do perfil
    if not request.user.is_authenticated or request.user.id != int(id):
        return redirect('receitas:homepage')  # ou mostre uma página de erro/permissão negada

    usuario = get_object_or_404(Usuario, pk=id)

    contexto = {
        'usuario': usuario,
        'titulo_janela': 'Perfil',
        'titulo_pagina': 'Perfil do Usuário',
    }

    return render(request, 'usuarios/perfil.html', contexto)

def login(request):
    """Função de realizar login

    Args:
        request (HttpRequest): A solicitação HTTP recebida.

    Returns:
        _type_: httpResponse: A resposta HTTP com a página de login.
    """
    #se o método for post, tenta logar o usuario
    if request.method == 'POST':
        formulario = UsuarioLoginForm(request.POST)
        if formulario.is_valid():
            auth_login(request, formulario.user)
            return redirect('receitas:homepage')

    #se não, apenas mostra o formulário de login
    else:
        formulario = UsuarioLoginForm()

    #conteúdo do contexto para renderizar o template
    contexto = {
        'formulario': formulario,
        'titulo_janela': 'Login',
        'titulo_pagina': 'Entrar',
    }

    #renderiza o template de login
    return render(request, 'usuarios/login.html', contexto)


class UsuarioCreateView(View):
    """View de criação de usuário

    Args:
        View (class): Classe base para views baseadas em classe.
    """
    def get(self, request, *args, **kwargs):
        """Exibe o formulário de criação de usuário

        Args:
            request (HttpRequest): A solicitação HTTP recebida.

        Returns:
            _type_: HttpResponse: A resposta HTTP com o formulário de criação de usuário.
        """
        contexto = { 'formulario': CustomUserCreationForm,
                     'titulo_janela' : 'Cadastro',
                    'titulo_pagina': 'Cadastrar Usuário',
                    'botao' : 'Cadastrar',}

        return render(request, "usuarios/cadastro.html", contexto)

    def post(self, request, *args, **kwargs):
        """função de postar o formulario de criação de usuario

        Args:
            request (HttpRequest): A solicitação HTTP recebida.

        Returns:
            HttpResponse: A resposta HTTP com o formulário de criação de usuário.
        """

        formulario = CustomUserCreationForm(request.POST)

        if formulario.is_valid():
            usuario = formulario.save()
            usuario.save()
            return HttpResponseRedirect(reverse_lazy("receitas:homepage"))

        else:
            contexto = {'formulario': formulario, 'mensagem': 'Erro ao completar o cadastro!'}
            return render(request, "usuarios/cadastro.html", contexto)

class UsuarioUpdateView(View):
    """View de atualização de usuário

    Args:
        View (class): Classe base para views baseadas em classe.
    """
    def get(self, request, id, *args, **kwargs):
        
        """Exibe o formulário de atualização de usuário

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            id (int): O ID do usuário a ser atualizado.

        Returns:
            HttpResponse: A resposta HTTP com o formulário de atualização de usuário.
        """
        # Garante que o usuário está autenticado e é o dono do perfil
        if not request.user.is_authenticated or request.user.id != int(id):
            return redirect('receitas:homepage')  # ou mostre uma página de erro/permissão negada
        
        usuario = get_object_or_404(Usuario, pk=self.kwargs['id'])

        formulario = UsuarioUpdateForm(instance=usuario)

        contexto = {
            'formulario': formulario,
            'usuario': usuario,
            'titulo_janela': 'Atualizar Perfil',
            'titulo_pagina': 'Atualizar Dados do Usuário',
            'botao': 'Atualizar Perfil',
        }
        return render(request, 'usuarios/atualiza.html', contexto)

    def post(self, request, id, *args, **kwargs):
        """Atualiza os dados do usuário

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            id (int): O ID do usuário a ser atualizado.

        Returns:
            HttpResponse: A resposta HTTP com o formulário de atualização de usuário.
        """
        # Garante que o usuário está autenticado e é o dono do perfil
        if not request.user.is_authenticated or request.user.id != int(id):
            return redirect('receitas:homepage')  # ou mostre uma página de erro/permissão negada
            
        usuario = get_object_or_404(Usuario, pk=self.kwargs['id'])

        formulario = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse_lazy('usuarios:perfil', kwargs={'id': id}))

        else:
            contexto = {
                'formulario': formulario,
                'usuario': usuario,
                'titulo_janela': 'Atualizar Perfil',
                'titulo_pagina': 'Atualizar Dados do Usuário',
                'botao': 'Atualizar Perfil',
            }

            return render(request, 'usuarios/atualiza.html', contexto)

class UsuarioDeleteView(View):
    """View de deletar usuário

    Args:
        View (class): Classe base para views baseadas em classe.
    """
    def get(self, request, id, *args, **kwargs):
        """Exibe a confirmação de deleção do usuário

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            id (int): O ID do usuário a ser deletado.

        Returns:
            HttpResponse: A resposta HTTP com a confirmação de deleção do usuário.
        """
        # Garante que o usuário está autenticado e é o dono do perfil
        if not request.user.is_authenticated or request.user.id != int(id):
            return redirect('receitas:homepage')  # ou mostre uma página de erro/permissão negada
        
        usuario = get_object_or_404(Usuario, pk=self.kwargs['id'])

        contexto = {
            'usuario': usuario,
            'titulo_janela': 'Deletar conta',
            'titulo_pagina': 'Deletar Perfil do Usuário',
            'botao': 'Deletar minha conta',
        }

        return render(request, "usuarios/deletar.html", contexto)

    def post(self, request, id, *args, **kwargs):
        """Realiza a deleção do usuário

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            id (int): O ID do usuário a ser deletado.

        Returns:
            HttpResponse: A resposta HTTP redirecionando para a página de login.
        """
        # Garante que o usuário está autenticado e é o dono do perfil
        if not request.user.is_authenticated or request.user.id != int(id):
            return redirect('receitas:homepage')  # ou mostre uma página de erro/permissão negada
        
        usuario = get_object_or_404(Usuario, pk=self.kwargs['id'])
        usuario.delete()
        return HttpResponseRedirect(reverse_lazy("usuarios:login"))

class ReceitaListView(View):

    """View de listar as receitas do usuário
    """
    def get(self, request, id, *args, **kwargs):
        """Exibe as receitas do usuário

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            id (int): O ID do usuário cujas receitas serão exibidas.

        Returns:
            HttpResponse: A resposta HTTP com as receitas do usuário.
        """
        # Garante que o usuário está autenticado e é o dono do perfil
        if not request.user.is_authenticated or request.user.id != int(id):
            return redirect('receitas:homepage')  # ou mostre uma página de erro/permissão negada
        
        usuario = Usuario.objects.get(pk=self.kwargs['id'])

        receitas = Receita.objects.filter(autor=usuario)

        contexto = {
            'usuario': usuario,
            'receitas': receitas,
            'titulo_janela': 'Minhas Receitas',
            'titulo_pagina': 'Receitas do Usuário',
        }

        return render(request, "usuarios/ver_minhas_receitas.html", contexto)

class MyPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    """View para alteração de senha do usuário

    Args:
        PasswordChangeView (class): Classe base para views de alteração de senha.
    """
    
    template_name = 'usuarios/password_change_form.html'
    success_url = reverse_lazy('usuarios:sec-password-change-done')

class MyPasswordChangeDoneView(LoginRequiredMixin,PasswordChangeDoneView):
    """View para confirmação de alteração de senha do usuário

    Args:
        PasswordChangeDoneView (class): Classe base para views de confirmação de alteração de senha.
    """
    template_name = 'usuarios/password_change_done.html'