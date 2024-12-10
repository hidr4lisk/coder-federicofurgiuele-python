from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario, Libro
from .forms import LibroForm

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
        return redirect('crear_usuario')  
    
    return render(request, "biblioteca/crear_usuario.html")

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "biblioteca/listar_usuarios.html", {"usuarios": usuarios})

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    messages.success(request, f"El usuario {usuario.nombre} ha sido eliminado correctamente.")
    return redirect("listar_usuarios")

def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro se ha creado exitosamente.')
            return redirect('crear_libro')
    else:
        form = LibroForm()

    return render(request, 'biblioteca/crear_libro.html', {'form': form})