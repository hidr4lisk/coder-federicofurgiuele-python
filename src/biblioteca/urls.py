from django.urls import path
from . import views, authentication

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("crear_usuario/", views.crear_usuario, name="crear_usuario"),
    path("login/", authentication.login_view, name="login"),
    path("logout/", authentication.logout_view, name="logout"),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('crear_libro/', views.crear_libro, name='crear_libro'),
    path('listar_libros/', views.listar_libros, name='listar_libros'),
    path('crear_prestamo/', views.crear_prestamo, name='crear_prestamo'),
    path('listar_prestamos/', views.listar_prestamos, name='listar_prestamos'),
    path('registrar_devolucion/<int:prestamo_id>/', views.registrar_devolucion, name='registrar_devolucion'),
    path('usuario/modificar/<int:usuario_id>/', views.modificar_usuario, name='modificar_usuario'),
    path('libro/modificar/<int:libro_id>/', views.modificar_libro, name='modificar_libro'),
    path('libro/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('eliminar_prestamos_devueltos/', views.eliminar_prestamos_devueltos, name='eliminar_prestamos_devueltos'),
]
