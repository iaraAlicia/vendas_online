from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('nova/', views.nova_venda, name='nova'),
    path('comprovante/<int:venda_id>/', views.comprovante, name='comprovante'),
    path('historico/', views.historico, name='historico'),
    path('', views.index, name='index'),
]
