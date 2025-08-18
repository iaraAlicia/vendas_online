# tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from produtos.models import Produto
from clientes.models import Cliente

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="user", password="123")

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="123", is_staff=True)

@pytest.fixture
def cliente(db, user):
    # Ajuste os campos obrigatórios de Cliente se houver
    return Cliente.objects.create(user=user)

@pytest.fixture
def produto(db):
    # Ajuste os campos obrigatórios de Produto se houver
    return Produto.objects.create(
        nome="Produto X",
        descricao="Desc",
        preco=100,    # se for DecimalField, ok também
        estoque=10
    )

@pytest.fixture
def auth_client(client, user):
    client.login(username="user", password="123")
    return client

@pytest.fixture
def staff_client(client, staff_user):
    client.login(username="staff", password="123")
    return client
