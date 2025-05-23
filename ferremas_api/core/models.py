from django.db import models
import requests


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    region = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

class StockSucursal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # USD

    class Meta:
        unique_together = ('producto', 'sucursal')

    def __str__(self):
        return f"{self.producto.nombre} en {self.sucursal.nombre}: {self.cantidad} unidades"

    def obtener_valor_dolar(self):
        try:
            api_key = "8ce3ef513b90b3f280dc4eec"
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            clp_rate = data['conversion_rates']['CLP']
            return 1 / clp_rate  # CLP → USD
        except Exception as e:
            print("Error al obtener tipo de cambio:", e)
            return None

    def save(self, *args, **kwargs):
        tasa = self.obtener_valor_dolar()
        if tasa:
            self.precio_usd = round(float(self.precio) / tasa, 2)  # Asegúrate de que esté dividiendo si CLP -> USD
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sucursal.nombre} - {self.producto.nombre}"

class Pedido(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('despachado', 'Despachado'),
    ], default='pendiente')

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # USD

    def obtener_valor_dolar(self):
        try:
            api_key = "8ce3ef513b90b3f280dc4eec"
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            clp_rate = data['conversion_rates']['CLP']
            return 1 / clp_rate  # CLP → USD
        except Exception as e:
            print("Error al obtener tipo de cambio:", e)
            return None

    def save(self, *args, **kwargs):
        tasa = self.obtener_valor_dolar()
        if tasa:
            self.precio_usd = round(float(self.precio_unitario) * tasa, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
