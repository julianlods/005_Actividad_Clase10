from django.db import models

# Clase para los contenedores (ubicaciones)
class Contenedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Ejemplo: 'Heladera', 'Alacena'
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional

    def __str__(self):
        return self.nombre

# Clase para los productos
class Producto(models.Model):
    UNIDADES_DE_MEDIDA = [
        ('UN', 'Unidades'),
        ('KG', 'Kilogramos'),
        ('LT', 'Litros'),
        ('GR', 'Gramos'),
    ]

    nombre = models.CharField(max_length=100)  # Ejemplo: 'Tomate', 'Papa'
    unidad_medida = models.CharField(max_length=2, choices=UNIDADES_DE_MEDIDA, default='UN')  # Unidad de medida
    fecha_vencimiento = models.DateField()  # Fecha de vencimiento del producto
    fecha_ingreso = models.DateField(auto_now_add=True)  # Fecha automática al ingresar
    cantidad_ingresada = models.PositiveIntegerField(default=0)  # Cantidad ingresada inicialmente
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE, related_name='productos')  # Relación con el contenedor

    def __str__(self):
        return f"{self.nombre} - {self.cantidad_ingresada} {self.get_unidad_medida_display()} en {self.contenedor.nombre}"

# Clase para registrar consumos (egresos de stock)
class Consumo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='consumos')  # Producto relacionado
    cantidad = models.PositiveIntegerField()  # Cantidad consumida
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora del consumo

    def __str__(self):
        return f"Consumo de {self.cantidad} {self.producto.nombre} el {self.fecha}"

    def save(self, *args, **kwargs):
        # Validar si hay suficiente stock antes de registrar el consumo
        if self.cantidad > self.producto.cantidad_ingresada:
            raise ValueError("No hay suficiente stock para este consumo.")
        # Reducir la cantidad ingresada del producto
        self.producto.cantidad_ingresada -= self.cantidad
        self.producto.save()
        super().save(*args, **kwargs)
