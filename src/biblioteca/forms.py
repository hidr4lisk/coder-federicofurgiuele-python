from django import forms
from .models import Libro, Prestamo

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn']  
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.disponible = True

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario']

        widgets = {
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'})
        }

