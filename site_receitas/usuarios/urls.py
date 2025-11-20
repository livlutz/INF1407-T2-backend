from django.urls import path, include
from usuarios import views
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

schema_view = yasg_schema_view(
    openapi.Info(
        title="API de Usuários",
        default_version='v1',
        description="API para gerenciamento de usuários",
        contact=openapi.Contact(email="contato@receitas.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define o namespace para as URLs do aplicativo de usuários
app_name = 'usuarios'

# Define as rotas URL para o aplicativo de usuários
urlpatterns = [
    path('cadastro/', views.UsuarioCreateView.as_view(), name='cadastro'), # rota de cadastro
    path('perfil/<int:id>/', views.PerfilView.as_view(), name='perfil'), # rota de perfil
    path('perfil/atualizar/<int:id>/', views.UsuarioUpdateView.as_view(), name='atualizar_perfil'), # rota de atualizar perfil
    path('perfil/deletar/<int:id>/', views.UsuarioDeleteView.as_view(), name='deletar'), # rota de deletar usuario
    path('perfil/receitas/<int:id>/', views.ReceitasUsuarioView.as_view(), name='minhas_receitas'), # rota de receitas do usuario

    # URLs para o swagger
    path('docs/', include_docs_urls(title='Documentação da API Usuários')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include(routers.DefaultRouter().urls)),
    path('openapi', get_schema_view(title="API para Usuários", description="API para gerenciamento de usuários"), name='openapi-schema'),
]