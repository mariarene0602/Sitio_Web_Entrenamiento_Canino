# app_Entrenamiento_Canino/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    fecha_suscripcion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de suscripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores"
    
    def __str__(self):
        return self.email

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=150, unique=True)
    direccion = models.CharField(max_length=200)
    
    # AGREGA ESTO:
    fecha_registro = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Perro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10)
    
    # === AGREGA ESTOS 3 CAMPOS NUEVOS ===
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # Usamos 'tamano' (sin ñ) para evitar problemas, o 'tamanio'
    tamano = models.CharField(max_length=20, null=True, blank=True) 
    comportamiento = models.TextField(null=True, blank=True)
    # ====================================

    def __str__(self):
        return f"{self.nombre} ({self.raza})"


class Entrenador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True) # Nuevo
    especialidad = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100, blank=True)   # Nuevo
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    experiencia = models.IntegerField(default=0)            # Nuevo
    tarifa_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Nuevo
    bio = models.TextField(blank=True) # Se usará para biografía
    horario_disponibilidad = models.CharField(max_length=200, blank=True) # Nuevo
    foto = models.ImageField(upload_to='entrenadores/', null=True, blank=True) # Nuevo
    disponible = models.BooleanField(default=True) # Nuevo

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField(help_text="Duración en horas")
    nivel = models.CharField(max_length=20, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    imagen = models.ImageField(upload_to='cursos/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def puede_editar(self, usuario):
        """Verifica si un usuario puede editar este curso"""
        if es_administrador(usuario):
            return True
        # Otras lógicas de permisos
        return False
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


# Asegúrate de que Curso esté definido antes que Oferta o usa 'Curso' en comillas
class Oferta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    porcentaje_descuento = models.IntegerField()
    fecha_limite = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    # === CAMPOS NUEVOS ===
    # 1. Conexión con el Curso (Opcional, por si quieres ofertas generales)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    
    # 2. Imagen de la oferta
    imagen = models.ImageField(upload_to='ofertas/', null=True, blank=True)
    # =====================

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.porcentaje_descuento}%"


class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, null=True, blank=True)
    entrenador = models.ForeignKey(Entrenador, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    notas = models.CharField(max_length=255, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, default='pendiente', choices=[
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ])

    def __str__(self):
        return f"Cita de {self.cliente} el {self.fecha}"


class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default="pendiente")

    def __str__(self):
        return f"Compra #{self.id} - {self.cliente}"


class Pago(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=50)
    referencia = models.CharField(max_length=100)
    estado_pago = models.CharField(max_length=20)

    def __str__(self):
        return f"Pago #{self.id} - {self.estado_pago}"


# models.py - versión actualizada del modelo Testimonio
class Testimonio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    contenido = models.TextField(verbose_name="Testimonio")
    calificacion = models.IntegerField(
        default=5,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name="Calificación"
    )
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Curso relacionado")
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de creación")
    aprobado = models.BooleanField(default=False, verbose_name="Aprobado")
    destacado = models.BooleanField(default=False, verbose_name="Destacado")
    
    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Testimonio de {self.cliente} - {self.calificacion}★"
    
# Método para verificar permisos
def es_administrador(usuario):
    """
    Verifica si un usuario tiene permisos de administración
    """
    return (
        usuario.is_authenticated and 
        usuario.is_active and 
        (usuario.is_staff or usuario.is_superuser)
    )
