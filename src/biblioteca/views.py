from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .models import Usuario, Libro, Prestamo
from .forms import LibroForm, PrestamoForm, UsuarioForm

def index(request):
    return render(request, "biblioteca/index.html")

def about(request):
    return render(request, "biblioteca/about.html")

@login_required
def crear_usuario(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        
        # Crear el usuario
        Usuario.objects.create(nombre=nombre, email=email, telefono=telefono)
        return redirect('listar_usuarios')  
    
    return render(request, "biblioteca/crear_usuario.html")

@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.prefetch_related('prestamos').all()
    return render(request, "biblioteca/listar_usuarios.html", {"usuarios": usuarios})

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    messages.success(request, f"El usuario {usuario.nombre} ha sido eliminado correctamente.")
    return redirect("listar_usuarios")

@login_required
def modificar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f"El usuario {usuario.nombre} ha sido actualizado correctamente.")
            return redirect("listar_usuarios")
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, "biblioteca/modificar_usuario.html", {"form": form, "usuario": usuario})

@login_required
def crear_libro(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Libro creado con éxito.")
            return redirect('listar_libros')
    else:
        form = LibroForm()
    
    return render(request, 'biblioteca/crear_libro.html', {'form': form})

@login_required
def modificar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if not libro.disponible:
        messages.error(request, f"El libro '{libro.titulo}' no se puede modificar porque está prestado.")
        return redirect("listar_libros")
    
    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"El libro '{libro.titulo}' ha sido actualizado correctamente.")
            return redirect("listar_libros")
    else:
        form = LibroForm(instance=libro)
    
   
    return render(request, "biblioteca/modificar_libro.html", {
        "form": form,
        "libro": libro,
        "disponible": libro.disponible
    })

def listar_libros(request):
    libros = Libro.objects.all()  
    return render(request, 'biblioteca/listar_libros.html', {'libros': libros})

@login_required
def crear_prestamo(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            libro = form.cleaned_data['libro']
            
            if not libro.disponible:
                messages.error(request, f"El libro '{libro.titulo}' no está disponible para préstamo.")
                return render(request, 'biblioteca/crear_prestamo.html', {'form': form})
            
            form.save()
            libro.disponible = False
            libro.save()
            messages.success(request, f"El libro '{libro.titulo}' ha sido prestado a {form.cleaned_data['usuario'].nombre}.")
            return redirect('listar_prestamos')
    else:
        form = PrestamoForm()

    return render(request, 'biblioteca/crear_prestamo.html', {'form': form})


@login_required
def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "biblioteca/listar_prestamos.html", {"prestamos": prestamos})

@login_required
def registrar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    if prestamo.fecha_devolucion:
        messages.warning(request, "Este libro ya fue devuelto.")
    else:
        prestamo.fecha_devolucion = now().date()
        prestamo.libro.disponible = True
        prestamo.libro.save()
        prestamo.save()
        messages.success(request, f"Devolución registrada para el libro '{prestamo.libro.titulo}'.")
    
    return redirect("listar_prestamos")

@login_required
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if not libro.disponible:
        messages.error(request, f"El libro '{libro.titulo}' no se puede eliminar porque está prestado.")
        return redirect("listar_libros")
    
    libro.delete()
    messages.success(request, f"El libro '{libro.titulo}' ha sido eliminado correctamente.")
    return redirect("listar_libros")

@login_required
def eliminar_prestamos_devueltos(request):
    if request.method == 'POST':
        Prestamo.objects.filter(fecha_devolucion__isnull=False).delete()
        messages.success(request, "Se han eliminado todos los préstamos devueltos.")
    return redirect('listar_prestamos') 