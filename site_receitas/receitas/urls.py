from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from receitas import views

#definindo o nome da aplicacao
app_name = 'receitas'

# Guarda as rotas da aplicacao receitas
urlpatterns = [
    path('', views.PubReceitasListView.as_view(), name = 'homepage'), #rota da homepage
    path('receita/<int:id>/', views.VerReceita.as_view(), name = 'ver_receita'), #rota para ver uma receita especifica
    path('criar_receita/', views.ReceitasCreateView.as_view(), name='criar_receita'), #rota para criar uma nova receita
    path('editar_receita/<int:id>/', views.ReceitasUpdateView.as_view(), name='editar_receita'), #rota para editar uma receita existente
    path('deletar_receita/<int:id>/', views.ReceitasDeleteView.as_view(), name='deletar_receita'), #rota para deletar uma receita existente
]

# Configuracao para servir arquivos de media durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)