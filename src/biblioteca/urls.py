from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("crear_usuario/", views.crear_usuario, name="crear_usuario"),
    path('listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('crear_libro/', views.crear_libro, name='crear_libro'),
]
