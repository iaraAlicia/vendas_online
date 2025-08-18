from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/index.html', {'produtos': produtos})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista.html', {'produtos': produtos})

def novo_produto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        preco = request.POST['preco']
        estoque = request.POST['estoque']
        imagem = request.FILES.get('imagem')  # NOVO
        Produto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            imagem=imagem
        )
        return redirect('produtos:lista')
    return render(request, 'produtos/formulario.html')


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.nome = request.POST['nome']
        produto.descricao = request.POST['descricao']
        produto.preco = request.POST['preco']
        produto.estoque = request.POST['estoque']
        if 'imagem' in request.FILES:
            produto.imagem = request.FILES['imagem']
        produto.save()
        return redirect('produtos:lista')
    return render(request, 'produtos/formulario.html', {'produto': produto})


def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('produtos:lista')
