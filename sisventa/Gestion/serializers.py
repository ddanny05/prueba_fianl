from rest_framework import serializers
from .models import Clientes,Vendedores,Productos,Proveedores,DetalleVentas,Ventas

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'

        
