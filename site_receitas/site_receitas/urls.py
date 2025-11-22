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
from django.urls import path, include
from django.conf import settings
from site_receitas import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="API das Receitas",
        default_version='v1',
        description="Documentação da API das Receitas",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="llutz@aluno.puc-rio.br"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #seria bom renomear o admin ou excluir, porem sem esse path nao conseguimos acessar o django admin
    path("admin/", admin.site.urls, name = 'admin'),

    # Redirect root to swagger
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),

    # Links para as URLs de autenticação do Django
    #path('password_reset/', PasswordResetView.as_view(template_name='usuarios/password_reset_form.html', email_template_name='usuarios/password_reset_email.html'), name='password_reset'), #rota de reset de senha
    #path('password_reset/done/', PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'), #rota de reset de senha concluída
    #path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'), #rota de confirmação de reset de senha
    #path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'), #rota de reset de senha completa

    # Links para as URLs de receitas
    path('receitas/', include('receitas.urls', namespace='receitas')),

    # Links para as URLs de usuários
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),

    # Links para as URLs de accounts
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # URLs para o swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from STATICFILES_DIRS (where favicon.ico is located)
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])