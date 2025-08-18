
# tests/test_loja_views.py
import pytest
from django.urls import reverse
from vendas.models import Venda, ItemVenda
from produtos.models import Produto

@pytest.mark.django_db
def test_produtos_sem_query_mostra_estoque(client, produto):
    url = reverse("loja:produtos")
    resp = client.get(url)
    assert resp.status_code == 200
    assert produto.nome in resp.content.decode()

@pytest.mark.django_db
def test_produtos_com_query_filtra(client, produto):
    url = reverse("loja:produtos")
    resp = client.get(url, {"q": "Produto X"})
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "Produto X" in html

@pytest.mark.django_db
def test_adicionar_ao_carrinho_post(client, produto):
    url = reverse("loja:adicionar", args=[produto.id])
    resp = client.post(url, {"quantidade": 2})
    assert resp.status_code == 302
    sess = client.session
    assert str(produto.id) in sess["carrinho"]
    assert sess["carrinho"][str(produto.id)] == 2

@pytest.mark.django_db
def test_carrinho_precisa_login(client):
    url = reverse("loja:carrinho")
    resp = client.get(url)
    assert resp.status_code in (302, 301)  # redirect para login
    # opcional: assert "login" in resp.url

@pytest.mark.django_db
def test_carrinho_lista_itens_e_total(auth_client, produto):
    # Prepara a sessão
    sess = auth_client.session
    sess["carrinho"] = {str(produto.id): 3}
    sess.save()

    url = reverse("loja:carrinho")
    resp = auth_client.get(url)
    assert resp.status_code == 200
    html = resp.content.decode()
    assert produto.nome in html
    # total esperado = preco * 3
    assert str(produto.preco * 3) in html

@pytest.mark.django_db
def test_remover_do_carrinho(auth_client, produto):
    sess = auth_client.session
    sess["carrinho"] = {str(produto.id): 1}
    sess.save()
    url = reverse("loja:remover", args=[produto.id])
    resp = auth_client.get(url)
    assert resp.status_code == 302
    assert str(produto.id) not in auth_client.session.get("carrinho", {})

@pytest.mark.django_db
def test_finalizar_compra_ok(client, user, cliente, produto):
    client.login(username="user", password="123")
    # carrinho com 2 unidades
    sess = client.session
    sess["carrinho"] = {str(produto.id): 2}
    sess.save()

    url = reverse("loja:finalizar")
    resp = client.get(url)
    assert resp.status_code == 200
    assert "loja/finalizado.html" in [t.name for t in resp.templates]

    # Verifica venda e item
    assert Venda.objects.count() == 1
    v = Venda.objects.first()
    assert ItemVenda.objects.count() == 1
    item = ItemVenda.objects.first()
    assert item.venda == v
    assert item.produto == produto
    assert item.quantidade == 2

    # Estoque atualizado
    produto.refresh_from_db()
    assert produto.estoque == 8  # 10 - 2

@pytest.mark.django_db
def test_finalizar_compra_sem_estoque_renderiza_erro(client, user, cliente, produto):
    client.login(username="user", password="123")
    sess = client.session
    sess["carrinho"] = {str(produto.id): 999}  # maior que estoque
    sess.save()

    url = reverse("loja:finalizar")
    resp = client.get(url)
    assert resp.status_code == 200
    assert "loja/erro_estoque.html" in [t.name for t in resp.templates]
