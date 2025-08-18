# tests/test_core_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_redirect_staff(staff_client):
    url = reverse("index")
    resp = staff_client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse("dashboard")

@pytest.mark.django_db
def test_home_redirect_usuario_com_cliente(client, user, cliente):
    client.login(username="user", password="123")
    url = reverse("index")
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse("loja:area_cliente")

@pytest.mark.django_db
def test_dashboard_staff_ok(staff_client):
    url = reverse("dashboard")
    resp = staff_client.get(url)
    # Renderiza 'index.html' com contexto
    assert resp.status_code == 200
    assert "index.html" in [t.name for t in resp.templates]

@pytest.mark.django_db
def test_dashboard_nao_staff_redireciona_login_admin(auth_client):
    url = reverse("dashboard")
    resp = auth_client.get(url)
    # @staff_member_required redireciona pro admin login
    assert resp.status_code == 302
    assert "/admin/login/" in resp.url
