from django.shortcuts import render, redirect, get_object_or_404
from clientes.models import Cliente
from produtos.models import Produto
from .models import Venda, ItemVenda
import json
from django.contrib import messages
from django.utils.timezone import now

from django.shortcuts import render

def index(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_produtos': Produto.objects.count(),
        'total_vendas': Venda.objects.count(),
    }
    return render(request, 'index.html', context)


def nova_venda(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            itens_json = request.POST.get('itens')
            cliente = get_object_or_404(Cliente, id=cliente_id)

            itens = json.loads(itens_json)
            if not itens:
                messages.error(request, 'Nenhum produto foi selecionado.')
                return redirect('vendas:nova')

            venda = Venda.objects.create(cliente=cliente)

            for item in itens:
                produto = get_object_or_404(Produto, id=item['id'])
                qtd = int(item['quantidade'])

                if qtd > produto.estoque:
                    messages.error(request, f'Estoque insuficiente para {produto.nome}')
                    venda.delete()
                    return redirect('vendas:nova')

                ItemVenda.objects.create(venda=venda, produto=produto, quantidade=qtd)
                produto.estoque -= qtd
                produto.save()

            return redirect('vendas:comprovante', venda_id=venda.id)
        
        except Exception as e:
            messages.error(request, f'Erro ao processar a venda: {str(e)}')
            return redirect('vendas:nova')

    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'vendas/nova_venda.html', {'clientes': clientes, 'produtos': produtos})

def comprovante(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    return render(request, 'vendas/comprovante.html', {'venda': venda})

def historico(request):
    vendas = Venda.objects.all().order_by('-data')  # ordena da mais recente para a mais antiga
    return render(request, 'vendas/historico.html', {'vendas': vendas})



