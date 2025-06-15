from django.contrib import admin
from .models import Persona,Producto,Carrito,ItemCarrito
# Register your models here.
admin.site.register(Persona)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)