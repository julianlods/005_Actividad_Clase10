from django.shortcuts import render
from .models import Contenedor, Producto, Consumo

# Vista para el inicio
def inicio(request):
    return render(request, 'MiApp/inicio.html')

# Vista para mostrar los contenedores y los productos
def contenedores(request):
    contenedores = Contenedor.objects.all()  # Obtener todos los contenedores
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'MiApp/contenedores.html', {'contenedores': contenedores, 'productos': productos})

# Vista para gestionar los consumos (egresos de stock)
def consumos(request):
    consumos = Consumo.objects.all()  # Obtener todos los consumos
    productos = Producto.objects.all()  # Obtener los productos disponibles
    return render(request, 'MiApp/consumos.html', {'consumos': consumos, 'productos': productos})
