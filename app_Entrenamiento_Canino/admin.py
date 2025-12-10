# app_Entrenamiento_Canino/admin.py
from django.contrib import admin
from .models import Testimonio, Cliente, Perro, Entrenador, Curso, Oferta, Cita, Compra, Pago, Newsletter

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    # NOTA: Usa 'contenido' no 'testimonio', y 'fecha_creacion' no 'fecha'
    list_display = ['id', 'cliente', 'contenido_short', 'calificacion', 'curso', 'fecha_creacion', 'aprobado', 'destacado']
    list_filter = ['fecha_creacion', 'aprobado', 'destacado', 'calificacion', 'curso']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'contenido']
    list_editable = ['aprobado', 'destacado', 'calificacion']
    date_hierarchy = 'fecha_creacion'
    
    # Función para mostrar contenido corto en la lista
    def contenido_short(self, obj):
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    contenido_short.short_description = 'Contenido'
    
    fieldsets = (
        ('Información del Testimonio', {
            'fields': ('cliente', 'curso', 'contenido', 'calificacion')
        }),
        ('Estado y Visibilidad', {
            'fields': ('aprobado', 'destacado', 'fecha_creacion')
        }),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'correo', 'telefono', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'correo']

@admin.register(Perro)
class PerroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'raza', 'edad', 'sexo', 'cliente']
    list_filter = ['raza', 'sexo']

@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'especialidad', 'email', 'disponible']
    list_filter = ['especialidad', 'disponible']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'duracion', 'nivel', 'activo']
    list_filter = ['nivel', 'activo']

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'porcentaje_descuento', 'curso', 'fecha_limite', 'activo']
    list_filter = ['activo']

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'entrenador', 'fecha', 'hora', 'estado']
    list_filter = ['estado', 'fecha']

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'curso', 'fecha_compra', 'precio_final', 'estado']
    list_filter = ['estado', 'fecha_compra']

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['compra', 'fecha_pago', 'monto', 'metodo_pago', 'estado_pago']
    list_filter = ['estado_pago', 'metodo_pago']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'fecha_suscripcion', 'activo']
    list_filter = ['activo']