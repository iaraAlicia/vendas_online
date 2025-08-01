from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.lista_produtos, name='lista'),
    path('novo/', views.novo_produto, name='novo'),
    path('editar/<int:id>/', views.editar_produto, name='editar'),
    path('excluir/<int:id>/', views.excluir_produto, name='excluir'),
    path('', views.index, name='index'),
]
