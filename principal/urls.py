from django.urls import path
#from .views import inicio,acerca,contacto,lista_personas
from . import views
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
    path('personas/', views.lista_personas, name='lista_personas'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('aumentar/<int:producto_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir/<int:producto_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('registrar_producto/', views.registrar_producto, name='registrar_producto'),
    path('mis-productos/', views.mis_productos, name='mis_productos'),
    path('mis-productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('tienda/', views.gestionar_tienda, name='gestionar_tienda'),
    path('tienda/<int:usuario_id>/', views.ver_tienda, name='ver_tienda'),
]