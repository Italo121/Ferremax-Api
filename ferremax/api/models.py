from django.db import models

# Create your models here.

class Sucursal(model.Model):
    nombre = models.CharField(max_length=100)
    
class Marca(model.Model):
    nombre = models.CharField(max_length=100)
    
class Producto(model.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca,on_delete= models.CASCADE)
    
    precio = models.IntegerField 
    codigo_sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE)
    
    
