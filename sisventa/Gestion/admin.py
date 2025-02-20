from django.contrib import admin
from .models import Clientes,Proveedores,Productos,DetalleVentas,Ventas,Vendedores

admin.site.register(Clientes)
admin.site.register(Proveedores)
admin.site.register(Productos)
admin.site.register(DetalleVentas)
admin.site.register(Ventas)
admin.site.register(Vendedores)
