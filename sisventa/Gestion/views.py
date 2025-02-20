from django.shortcuts import render
from rest_framework import viewsets
from .models import Clientes, Productos, Proveedores,DetalleVentas, Ventas, Vendedores
from .serializers import ClientesSerializer
from rest_framework.permissions import AllowAny

class ClientesViewSet (viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [AllowAny] # Permitir que cualquiera pueda acceder a los datos

