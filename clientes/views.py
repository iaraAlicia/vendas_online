from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente

def index(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {'clientes': clientes})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {'clientes': clientes})

def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        Cliente.objects.create(nome=nome, email=email, telefone=telefone)
        return redirect('clientes:lista')
    return render(request, 'clientes/formulario.html')

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nome = request.POST['nome']
        cliente.email = request.POST['email']
        cliente.telefone = request.POST['telefone']
        cliente.save()
        return redirect('clientes:lista')
    return render(request, 'clientes/formulario.html', {'cliente': cliente})

def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('clientes:lista')

from django.shortcuts import render, redirect
from .forms import UsuarioForm, ClienteForm
from django.contrib.auth import authenticate, login

def cadastrar_cliente(request):
    if request.method == 'POST':
        form_user = UsuarioForm(request.POST)
        form_cliente = ClienteForm(request.POST)
        if form_user.is_valid() and form_cliente.is_valid():
            user = form_user.save(commit=False)
            user.set_password(user.password)
            user.save()
            cliente = form_cliente.save(commit=False)
            cliente.user = user
            cliente.save()
            login(request, user)
            return redirect('loja:produtos')  # após login
    else:
        form_user = UsuarioForm()
        form_cliente = ClienteForm()
    return render(request, 'clientes/cadastro.html', {
        'form_user': form_user,
        'form_cliente': form_cliente,
    })

