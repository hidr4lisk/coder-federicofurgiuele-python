from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .models import Usuario, Libro, Prestamo
from .forms import LibroForm, PrestamoForm

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

def listar_libros(request):
    libros = Libro.objects.all()  
    return render(request, 'biblioteca/listar_libros.html', {'libros': libros})

def crear_prestamo(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('listar_prestamos')  
    else:
        form = PrestamoForm()

    return render(request, 'biblioteca/crear_prestamo.html', {'form': form})

def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "biblioteca/listar_prestamos.html", {"prestamos": prestamos})

def registrar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    if prestamo.fecha_devolucion:
        messages.warning(request, "Este libro ya fue devuelto.")
    else:
        prestamo.fecha_devolucion = now().date()
        prestamo.save()
        messages.success(request, f"Devolución registrada para el libro '{prestamo.libro.titulo}'.")
    
    return redirect("listar_prestamos")