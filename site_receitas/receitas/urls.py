from receitas import views
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

schema_view = yasg_schema_view(
    openapi.Info(
        title="API das receitas",
        default_version='v1',
        description="Descrição da API das receitas",
        contact=openapi.Contact(email="llutz@aluno.puc-rio.br"),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#definindo o nome da aplicacao
app_name = 'receitas'

# Guarda as rotas da aplicacao receitas
urlpatterns = [
    path('', views.PubReceitasListView.as_view(), name='homepage'), #rota da homepage
    path('<int:id>/', views.VisibleReceitasListView.as_view(), name='receitas_visiveis'), #rota para listar receitas visiveis ao usuario autenticado
    path('receita/<int:id>/', views.VerReceita.as_view(), name='ver_receita'), #rota para ver uma receita especifica
    path('criar_receita/', views.ReceitasCreateView.as_view(), name='criar_receita'), #rota para criar uma nova receita
    path('editar_receita/<int:id>/', views.ReceitasUpdateView.as_view(), name='editar_receita'), #rota para editar uma receita
    path('deletar_receita/<int:id>/', views.ReceitasDeleteView.as_view(), name='deletar_receita'), #rota para deletar uma receita

    #URLs para o swagger
    #path('docs/', include_docs_urls(title='Documentação da API Receitas')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include(routers.DefaultRouter().urls)),
    path('openapi', get_schema_view(title="API para Receitas", description="API para gerenciamento de receitas"), name='openapi-schema'),
]
