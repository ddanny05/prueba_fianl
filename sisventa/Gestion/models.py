from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class Clientes(models.Model):
    cedula = models.CharField(max_length=10,primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
   
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'Clientes'

    def __str__(self):
        return f'{self.cedula } -- {self.nombre} -- {self.apellido}'

class Proveedores(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'Proveedores'
        

    def __str__(self):
        return f'{self.cedula} -- {self.nombre} -- {self.apellido}'

class Productos(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField()
    fecha_elaboracion = models.DateField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=30)
        
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'Productos'

    def __str__(self):
        return f'{self.codigo} -- {self.nombre}'

class Vendedores(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        db_table = 'Vendedores'
    
    def __str__(self):
        return f'{self.cedula} -- {self.nombre} -- {self.apellido}'


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'Ventas'
    
    def __str__(self):
        return f'{self.id_venta} -- {self.fecha}'

class DetalleVentas(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey('Ventas', on_delete=models.CASCADE)
    producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    iva = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        db_table = 'Detalle_Ventas'

    def save(self, *args, **kwargs):
        """Calcula subtotal, IVA y total antes de guardar"""

        # Verificar que la cantidad sea mayor a 0
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")

        # Verificar que haya stock disponible
        if self.producto.stock < self.cantidad:
            raise ValidationError(f"Stock insuficiente. Solo hay {self.producto.stock} unidades disponibles.")

        # Convertir el precio y porcentaje de IVA a Decimal
        precio_venta = Decimal(self.producto.precio_venta)
        porcentaje_iva = Decimal('0.12')  # Usar cadena para precisión Decimal

        # Cálculo del subtotal, IVA y total
        self.subtotal = self.cantidad * precio_venta
        self.iva = (self.subtotal * porcentaje_iva).quantize(Decimal('0.01'))  # Redondeo a 2 decimales
        self.total = (self.subtotal + self.iva).quantize(Decimal('0.01'))  # Redondeo a 2 decimales

        # Reducir stock del producto
        self.producto.stock -= self.cantidad
        self.producto.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id_detalle} - Venta: {self.venta.id_venta} - Producto: {self.producto.nombre} - subtotal {self.subtotal} - iva {self.iva}  - Total: {self.total}'