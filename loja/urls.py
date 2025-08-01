from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    path('', views.produtos, name='produtos'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('finalizar/', views.finalizar_compra, name='finalizar'),
    path('minha-conta/', views.area_cliente, name='area_cliente'),
]
