"""
URL configuration for site_receitas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from site_receitas import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    #seria bom renomear o admin ou excluir, porem sem esse path nao conseguimos acessar o django admin
    path("admin/", admin.site.urls, name = 'admin'),
    # Links para as URLs de autenticação do Django
    path('password_reset/', PasswordResetView.as_view(template_name='usuarios/password_reset_form.html', email_template_name='usuarios/password_reset_email.html'), name='password_reset'), #rota de reset de senha
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'), #rota de reset de senha concluída
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'), #rota de confirmação de reset de senha
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'), #rota de reset de senha completa
    # Links para as URLs de receitas
    path('', include('receitas.urls', namespace='receitas')),
    # Links para as URLs de usuários
    path('', include('usuarios.urls', namespace='usuarios')),
]