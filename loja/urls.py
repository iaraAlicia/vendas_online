from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    path('', views.produtos, name='produtos'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('remover/<int:produto_id>/', views.remover_do_carrinho, name='remover'),  
    path('finalizar/', views.finalizar_compra, name='finalizar'),
    path('minha-conta/', views.area_cliente, name='area_cliente'),
    path('nao-cliente/', views.nao_cliente, name='nao_cliente'),
    
    # path('gerar-pdf/<int:venda_id>/', views.gerar_pdf, name='gerar_pdf'),
    # path('excluir-venda/<int:venda_id>/', views.excluir_venda, name='excluir_venda'),
]
