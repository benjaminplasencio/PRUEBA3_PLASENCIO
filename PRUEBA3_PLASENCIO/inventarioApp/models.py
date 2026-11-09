from django.db import models

#Create your models here.

class CategoriaModel(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

from django.db import models

class ProductoModel(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre