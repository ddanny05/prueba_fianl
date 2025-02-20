from django.db import models
from django.core.exceptions import ValidationError

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
        return f'{self.ruc} -- {self.nombre} -- {self.apellido}'

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
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        db_table = 'Detalle_Ventas'
    def save(self, *args, **kwargs):
        """Calcula subtotal, IVA y total antes de guardar"""
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")

        self.subtotal = self.cantidad * self.precio  # Subtotal = cantidad * precio_unitario
        porcentaje_iva = 12  # IVA del 12% en Ecuador
        self.iva = self.subtotal * (porcentaje_iva / 100)  # IVA = subtotal * 0.12
        self.total = self.subtotal + self.iva  # Total = subtotal + IVA
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        db_table = 'Detalle_Ventas'

    def __str__(self):
        return f'{self.id_detalle} - Venta: {self.venta.id_venta} - Producto: {self.producto.nombre} - Total: {self.total}'
    
    def __str__(self):
        return f'{self.id_detalle} -- {self.venta}'
    

