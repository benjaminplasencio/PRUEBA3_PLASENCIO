from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ProductoModel
from .forms import ProductoForm, RegistroUsuarioForm 


def index(request):
    if request.user.is_authenticated:
        return redirect('listar_productos')
    
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('listar_productos')
        else:
            return render(request, 'index.html', {'error': 'Usuario o contraseña incorrectos'})
            
    return render(request, 'index.html')


@login_required
def salir(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')


@login_required
def listar_productos(request):
    query = request.GET.get('q', '')
    if query:
        productos = ProductoModel.objects.filter(nombre__icontains=query)
    else:
        productos = ProductoModel.objects.all()
        
    es_admin = request.user.is_superuser or request.user.username in ['administrador', 'superuser']
    
    return render(request, 'listar_productos.html', {
        'productos': productos,
        'query': query,
        'es_admin': es_admin
    })


@login_required
def agregar_producto(request):
    if not (request.user.is_superuser or request.user.username in ['administrador', 'superuser']):
        return redirect('listar_productos')

    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_productos')
    else:
        formulario = ProductoForm()

    return render(request, 'agregar_producto.html', {'formulario': formulario})


@login_required
def modificar_producto(request, id_producto):
    if not (request.user.is_superuser or request.user.username in ['administrador', 'superuser']):
        return redirect('listar_productos')

    producto = get_object_or_404(ProductoModel, id=id_producto)
    
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_productos')
    else:
        formulario = ProductoForm(instance=producto)

    return render(request, 'modificar_producto.html', {'formulario': formulario, 'producto': producto})


@login_required
def eliminar_producto(request, id_producto):
    if not (request.user.is_superuser or request.user.username in ['administrador', 'superuser']):
        return redirect('listar_productos')

    producto = get_object_or_404(ProductoModel, id=id_producto)
    
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')

    return render(request, 'eliminar_producto.html', {'producto': producto})

@login_required
def crear_usuario(request):
    if not (request.user.is_superuser or request.user.username in ['administrador', 'superuser']):
        return redirect('listar_productos')

    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            user = formulario.save(commit=False)
            
            
            if formulario.cleaned_data.get('es_administrador'):
                user.is_superuser = True
                user.is_staff = True
            
            user.save()
            return redirect('listar_productos')
    else:
        formulario = RegistroUsuarioForm()

    return render(request, 'crear_usuario.html', {'formulario': formulario})