
#from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Persona,Producto,Carrito,ItemCarrito,Tienda
from .carrito import Carrito
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ProductoForm,TiendaForm
from django.contrib.auth.models import User

def inicio(request):
    return render(request, 'principal/inicio.html')


def acerca(request):
    return render(request, 'principal/acerca.html')


def contacto(request):
    return render(request, 'principal/contacto.html')

def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, 'principal/lista_personas.html', {'personas': personas})

@login_required
def lista_productos(request):
    productos = Producto.objects.all().select_related('usuario__tienda')
    return render(request, 'principal/productos.html', {'productos': productos})

@login_required
def mis_productos(request):
    productos = Producto.objects.filter(usuario=request.user)
    return render(request, 'principal/mis_productos.html', {'productos': productos})

@login_required
def obtener_carrito(request):
    carrito_id = request.session.get("carrito_id")
    if carrito_id:
        carrito = get_object_or_404(Carrito, id=carrito_id)
    else:
        carrito = Carrito.objects.create()
        request.session["carrito_id"] = carrito.id
    return carrito

@login_required
@require_POST
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    # Aumenta la cantidad del producto
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    request.session['carrito'] = carrito
    return redirect('lista_productos')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    carrito_actualizado = False

    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.filter(pk=producto_id).first()
        if producto is None:
            # El producto ya no existe: eliminarlo del carrito
            del carrito[producto_id]
            carrito_actualizado = True
            continue

        subtotal = producto.precio * cantidad
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })
        total += subtotal

    if carrito_actualizado:
        request.session['carrito'] = carrito

    return render(request, 'principal/carrito.html', {
        'productos': productos,
        'total': total
    })

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    producto_id = str(producto_id)
    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')

@login_required
def aumentar_cantidad(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        carrito[producto_id] += 1
    else:
        carrito[producto_id] = 1

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


@login_required
def disminuir_cantidad(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        carrito[producto_id] -= 1
        if carrito[producto_id] <= 0:
            del carrito[producto_id]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Tienda.objects.create(usuario=usuario)
            login(request, usuario)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def registrar_producto(request):
    if not hasattr(request.user, 'tienda'):
        return redirect('gestionar_tienda')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'principal/registrar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, usuario=request.user)
    producto.delete()
    return redirect('mis_productos')

@login_required
def gestionar_tienda(request):
    tienda, creado = Tienda.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = TiendaForm(request.POST, instance=tienda)
        if form.is_valid():
            form.save()
            if creado:
                return redirect('registrar_producto')
            return redirect('mis_productos')
    else:
        form = TiendaForm(instance=tienda)

    return render(request, 'principal/gestionar_tienda.html', {'form': form})

def ver_tienda(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    productos = Producto.objects.filter(usuario=usuario)
    tienda = getattr(usuario, 'tienda', None)

    return render(request, 'principal/ver_tienda.html', {
        'usuario': usuario,
        'productos': productos,
        'tienda': tienda
    })