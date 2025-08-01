from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista'),
    path('novo/', views.novo_cliente, name='novo'),
    path('editar/<int:id>/', views.editar_cliente, name='editar'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir'),
    
    path('', views.index, name='index'),
    path('cadastro/', views.cadastrar_cliente, name='cadastro'),
]
