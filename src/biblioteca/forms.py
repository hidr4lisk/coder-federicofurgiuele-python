from django import forms
from .models import Libro, Prestamo

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn', 'disponible']

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario', 'fecha_devolucion']

        widgets = {
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'})
        }

