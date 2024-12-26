from django.db import models
from typing import Any
from django.db.models import QuerySet

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Type hint para el type checker
    prestamos: QuerySet[Any]
    
    def __str__(self):
        return self.nombre
        
    def tiene_prestamos_pendientes(self):
        return self.prestamos.filter(fecha_devolucion__isnull=True).exists()

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='prestamos'
    )
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.libro.titulo} prestado a {self.usuario.nombre}"