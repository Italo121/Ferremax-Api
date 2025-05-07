from django.db import models

# Create your models here.

class Sucursal(model.Model):
    nombre = models.CharField(max_length=100)
    
class Marca(model.Model):
    nombre = models.CharField(max_length=100)
    
class Producto(model.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca,on_delete= models.CASCADE)
    
    codigo_sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE)

class Precio(models.Model):
    producto = models.ForeignKey(Producto, related_name='precios', on_delete=models.CASCADE)
    fecha = models.DateTimeField()                                 
    valor = models.DecimalField(max_digits=10, decimal_places=2) 
    
    
