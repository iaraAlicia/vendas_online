from django.shortcuts import render, redirect, get_object_or_404
from produtos.models import Produto
from vendas.models import Venda, ItemVenda
from clientes.models import Cliente
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def produtos(request):
    lista = Produto.objects.filter(estoque__gt=0)
    return render(request, 'loja/produtos.html', {'produtos': lista})

@require_POST
def adicionar_ao_carrinho(request, produto_id):
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho = request.session.get('carrinho', {})
    carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + quantidade
    request.session['carrinho'] = carrinho
    return redirect('loja:carrinho')


@login_required
def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens = []
    total = 0
    for produto_id, qtd in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        subtotal = produto.preco * qtd
        total += subtotal
        itens.append({
            'produto': produto,
            'quantidade': qtd,  # Corrigido
            'subtotal': subtotal,
        })
    return render(request, 'loja/carrinho.html', {'itens': itens, 'total': total})

@login_required
def finalizar_compra(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('loja:carrinho')

    cliente = Cliente.objects.get(user=request.user)
    venda = Venda.objects.create(cliente=cliente)

    for produto_id, qtd in carrinho.items():
        produto = Produto.objects.get(id=produto_id)

        # Verifica se tem estoque suficiente
        if produto.estoque < qtd:
            return render(request, 'loja/erro_estoque.html', {
                'produto': produto,
                'quantidade_pedida': qtd,
                'estoque_disponivel': produto.estoque
            })

        # Cria o item da venda com quantidade correta
        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=qtd
        )

        # Atualiza o estoque do produto
        produto.estoque -= qtd
        produto.save()

    # Limpa o carrinho
    del request.session['carrinho']
    return render(request, 'loja/finalizado.html', {'venda': venda})
@login_required
def area_cliente(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        return render(request, 'loja/nao_cliente.html')

    vendas = Venda.objects.filter(cliente=cliente).order_by('-data')
    return render(request, 'loja/area_cliente.html', {
        'cliente': cliente,
        'vendas': vendas
    })

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
        request.session['carrinho'] = carrinho
    return redirect('loja:carrinho')