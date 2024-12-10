from django.shortcuts import render, redirect
from .models import Usuario

def index(request):
    return render(request, "biblioteca/index.html")

def about(request):
    return render(request, "biblioteca/about.html")

def crear_usuario(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        
        # Crear el usuario
        Usuario.objects.create(nombre=nombre, email=email, telefono=telefono)
        return redirect('index')  
    
    return render(request, "biblioteca/crear_usuario.html")