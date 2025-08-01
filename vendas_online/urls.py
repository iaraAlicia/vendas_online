"""
URL configuration for vendas_online project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from core.views import dashboard, redirecionar_usuario, index_publico
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página inicial pública (login inteligente: cliente/admin)
    path('', index_publico, name='index'),

    # Dashboard de administração (somente staff acessa)
    path('dashboard/', dashboard, name='dashboard'),

    # Login/Logout usando templates personalizados
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Apps
    path('produtos/', include('produtos.urls')),
    path('clientes/', include('clientes.urls')),
    path('vendas/', include('vendas.urls')),
    path('loja/', include('loja.urls')),
    
    # Redirecionamento pós login
    path('login-redirect/', redirecionar_usuario, name='login_redirect'),
]
