from django.shortcuts import render, redirect
from clientes.models import Cliente
from produtos.models import Produto
from vendas.models import Venda, ItemVenda

import calendar
from django.db.models import Sum
from decimal import Decimal
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden

def index_publico(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')  # ou para onde estiver seu dashboard
        else:
            return redirect('loja:area_cliente')
    return render(request, 'core/index.html')

def redirecionar_usuario(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        return redirect('loja:area_cliente')


@staff_member_required
def dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    # Contagens
    total_clientes = Cliente.objects.count()
    total_produtos = Produto.objects.count()
    total_vendas = Venda.objects.count()

    # Soma total faturado
    total_faturado = sum(v.total for v in Venda.objects.all())

    # Gráfico de vendas por mês
    meses_dict = defaultdict(Decimal)
    for v in Venda.objects.all():
        mes = v.data.strftime("%B/%Y")
        meses_dict[mes] += v.total

    meses = list(meses_dict.keys())
    valores = [float(valor) for valor in meses_dict.values()]

    # Gráfico de produtos mais vendidos
    produtos_data = ItemVenda.objects.values('produto__nome').annotate(qtd=Sum('quantidade')).order_by('-qtd')[:5]
    nomes_produtos = [p['produto__nome'] for p in produtos_data]
    quantidades_produtos = [p['qtd'] for p in produtos_data]

    context = {
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'total_vendas': total_vendas,
        'total_faturado': total_faturado,
        'meses': meses,
        'valores': valores,
        'nomes_produtos': nomes_produtos,
        'quantidades_produtos': quantidades_produtos,
    }

    return render(request, 'index.html', context)