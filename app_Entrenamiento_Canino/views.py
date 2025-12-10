# app_Entrenamiento_Canino/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Newsletter
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cliente, Perro, Curso, Compra, Entrenador, Oferta, Pago, Cita, Testimonio
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.db.models import Q
from django.db.models import Avg
import time
from django.shortcuts import redirect
from .forms import TestimonioForm

# ==================== VISTAS GENERALES ====================
def inicio_entrenamiento_canino(request):
    total_clientes = Cliente.objects.count()
    total_perros = Perro.objects.count()
    total_cursos = Curso.objects.count()
    total_citas = Cita.objects.count()
    
    return render(request, 'inicio.html', {
        'total_clientes': total_clientes,
        'total_perros': total_perros,
        'total_cursos': total_cursos,
        'total_citas': total_citas,
    })

# ==================== CLIENTES - CRUD COMPLETO ====================
def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'admin/crud/clientes/listar.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            telefono=request.POST['telefono'],
            correo=request.POST['correo'],
            direccion=request.POST['direccion']
        )
        return redirect('ver_clientes')
    return render(request, 'admin/crud/clientes/agregar.html')

@staff_member_required
def actualizar_cliente(request, id):
    # Obtener el cliente o dar error 404
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        # Actualizamos los campos
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')
        cliente.correo = request.POST.get('correo') # Ahora sí coincidirá con el HTML
        cliente.direccion = request.POST.get('direccion')
        
        # Guardamos en la BD
        cliente.save()
        
        # Opcional: Actualizar también los datos del Usuario de Django para mantener consistencia
        if cliente.usuario:
            cliente.usuario.email = cliente.correo
            cliente.usuario.first_name = cliente.nombre
            cliente.usuario.last_name = cliente.apellido
            cliente.usuario.save()
            
        return redirect('ver_clientes')
        
    return render(request, 'admin/crud/clientes/editar.html', {'cliente': cliente})

def borrar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'admin/crud/clientes/eliminar.html', {'cliente': cliente})

# ==================== PERROS - CRUD COMPLETO ====================
def ver_perros(request):
    perros = Perro.objects.all()
    return render(request, 'admin/crud/perros/listar.html', {'perros': perros})

@login_required
def agregar_perro(request):
    """Agregar un perro al perfil del cliente"""
    if request.method == 'POST':
        try:
            cliente = Cliente.objects.get(correo=request.user.email)
            
            perro_id = request.POST.get('perro_id')
            
            if perro_id:
                # Editar perro existente
                perro = Perro.objects.get(id=perro_id, cliente=cliente)
                perro.nombre = request.POST.get('nombre')
                perro.raza = request.POST.get('raza')
                perro.edad = request.POST.get('edad')
                perro.peso = request.POST.get('peso')
                perro.sexo = request.POST.get('sexo')
                perro.comportamiento = request.POST.get('comportamiento', '')
                perro.save()
                messages.success(request, 'Perro actualizado correctamente')
            else:
                # Crear nuevo perro
                Perro.objects.create(
                    cliente=cliente,
                    nombre=request.POST.get('nombre'),
                    raza=request.POST.get('raza'),
                    edad=request.POST.get('edad'),
                    peso=request.POST.get('peso'),
                    sexo=request.POST.get('sexo'),
                    comportamiento=request.POST.get('comportamiento', '')
                )
                messages.success(request, 'Perro agregado correctamente')
                
        except Cliente.DoesNotExist:
            messages.error(request, 'Primero completa tu perfil de cliente')
        except Perro.DoesNotExist:
            messages.error(request, 'El perro no existe o no tienes permisos')
    
    return redirect('perfil')

def actualizar_perro(request, id):
    perro = get_object_or_404(Perro, id=id)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        perro.cliente_id = request.POST['cliente']
        perro.nombre = request.POST['nombre']
        perro.raza = request.POST['raza']
        perro.edad = request.POST['edad']
        perro.sexo = request.POST['sexo']
        perro.save()
        return redirect('ver_perros')
    return render(request, 'admin/crud/perros/editar.html', {
        'perro': perro,
        'clientes': clientes
    })

from django.http import JsonResponse

@staff_member_required
def borrar_perro(request, id):
    # 1. Buscamos el perro
    perro = get_object_or_404(Perro, id=id)
    
    if request.method == 'POST':
        # 3. Si confirmaron (dieron clic al botón rojo del formulario), borramos
        perro.delete()
        return redirect('ver_perros')
    
    # 2. Si es la primera vez (GET), mostramos la página de confirmación
    return render(request, 'admin/crud/perros/eliminar.html', {'perro': perro})

# ==================== ENTRENADORES - CRUD COMPLETO ====================
def ver_entrenadores(request):
    entrenadores = Entrenador.objects.all()
    return render(request, 'admin/crud/entrenadores/listar.html', {'entrenadores': entrenadores})

def agregar_entrenador(request):
    if request.method == 'POST':
        try:
            # Capturamos TODOS los campos del formulario largo
            Entrenador.objects.create(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                email=request.POST.get('email'), # Corregido: usa 'email'
                telefono=request.POST.get('telefono'),
                titulo=request.POST.get('titulo'),
                especialidad=request.POST.get('especialidad'),
                experiencia=request.POST.get('experiencia') or 0,
                tarifa_hora=request.POST.get('tarifa_hora') or 0.0,
                bio=request.POST.get('biografia'), # El HTML usa name="biografia"
                horario_disponibilidad=request.POST.get('horario_disponibilidad'),
                disponible=request.POST.get('disponible') == 'on', # Checkbox
                foto=request.FILES.get('foto') # Captura la imagen
            )
            return redirect('ver_entrenadores')
        except Exception as e:
            # Si falla, imprimimos el error en consola y en pantalla
            print(f"Error: {e}")
            return render(request, 'admin/crud/entrenadores/agregar.html', {'error': str(e)})

    return render(request, 'admin/crud/entrenadores/agregar.html')

def actualizar_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    
    if request.method == 'POST':
        try:
            # Actualizamos los campos básicos
            entrenador.nombre = request.POST.get('nombre')
            entrenador.apellido = request.POST.get('apellido')
            entrenador.email = request.POST.get('email')  # <--- CORREGIDO: 'email'
            entrenador.telefono = request.POST.get('telefono')
            
            # Actualizamos los campos nuevos
            entrenador.titulo = request.POST.get('titulo')
            entrenador.especialidad = request.POST.get('especialidad')
            entrenador.experiencia = request.POST.get('experiencia') or 0
            entrenador.tarifa_hora = request.POST.get('tarifa_hora') or 0.0
            entrenador.bio = request.POST.get('bio')
            entrenador.horario_disponibilidad = request.POST.get('horario_disponibilidad')
            
            # Checkbox (si no viene, es False)
            entrenador.disponible = request.POST.get('disponible') == 'on'
            
            # Foto (Solo si se sube una nueva)
            if request.FILES.get('foto'):
                entrenador.foto = request.FILES.get('foto')
            
            entrenador.save()
            return redirect('ver_entrenadores')
            
        except Exception as e:
            return render(request, 'admin/crud/entrenadores/editar.html', {
                'entrenador': entrenador,
                'error': str(e)
            })

    return render(request, 'admin/crud/entrenadores/editar.html', {'entrenador': entrenador})

def borrar_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    if request.method == 'POST':
        entrenador.delete()
        return redirect('ver_entrenadores')
    return render(request, 'admin/crud/entrenadores/eliminar.html', {'entrenador': entrenador})

# ==================== CURSOS - CRUD COMPLETO ====================
def ver_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'admin/crud/cursos/listar.html', {'cursos': cursos})

def agregar_curso(request):
    if request.method == 'POST':
        Curso.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            precio=request.POST['precio'],
            duracion=request.POST['duracion'],
            nivel=request.POST['nivel']
        )
        return redirect('ver_cursos')
    return render(request, 'admin/crud/cursos/agregar.html')

def actualizar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.nombre = request.POST['nombre']
        curso.descripcion = request.POST['descripcion']
        curso.precio = request.POST['precio']
        curso.duracion = request.POST['duracion']
        curso.nivel = request.POST['nivel']
        curso.save()
        return redirect('ver_cursos')
    return render(request, 'admin/crud/cursos/editar.html', {'curso': curso})

def borrar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.delete()
        return redirect('ver_cursos')
    return render(request, 'admin/crud/cursos/eliminar.html', {'curso': curso})

# ==================== CITAS - CRUD COMPLETO ====================
def ver_citas(request):
    citas = Cita.objects.all()
    return render(request, 'admin/crud/citas/listar.html', {'citas': citas})

def agregar_cita(request):
    clientes = Cliente.objects.all()
    perros = Perro.objects.all()
    entrenadores = Entrenador.objects.all()
    
    if request.method == 'POST':
        perro_id = request.POST.get('perro', None)
        entrenador_id = request.POST.get('entrenador', None)
        
        Cita.objects.create(
            cliente_id=request.POST['cliente'],
            perro_id=perro_id if perro_id else None,
            entrenador_id=entrenador_id if entrenador_id else None,
            fecha=request.POST['fecha'],
            hora=request.POST['hora'],
            notas=request.POST.get('notas', '')
        )
        return redirect('ver_citas')
    
    return render(request, 'admin/crud/citas/agregar.html', {
        'clientes': clientes,
        'perros': perros,
        'entrenadores': entrenadores,
        'today': timezone.now().date()
    })

def actualizar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    clientes = Cliente.objects.all()
    perros = Perro.objects.all()
    entrenadores = Entrenador.objects.all()
    
    if request.method == 'POST':
        perro_id = request.POST.get('perro', None)
        entrenador_id = request.POST.get('entrenador', None)
        
        cita.cliente_id = request.POST['cliente']
        cita.perro_id = perro_id if perro_id else None
        cita.entrenador_id = entrenador_id if entrenador_id else None
        cita.fecha = request.POST['fecha']
        cita.hora = request.POST['hora']
        cita.notas = request.POST.get('notas', '')
        cita.save()
        return redirect('ver_citas')
    
    return render(request, 'admin/crud/citas/editar.html', {
        'cita': cita,
        'clientes': clientes,
        'perros': perros,
        'entrenadores': entrenadores
    })

def borrar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        cita.delete()
        return redirect('ver_citas')
    return render(request, 'admin/crud/citas/eliminar.html', {'cita': cita})

# ==================== COMPRAS - CRUD COMPLETO ====================
def ver_compras(request):
    compras = Compra.objects.all()
    return render(request, 'admin/crud/compras/listar.html', {'compras': compras})

def agregar_compra(request):
    clientes = Cliente.objects.all()
    cursos = Curso.objects.all()
    
    if request.method == 'POST':
        precio_base = float(request.POST['precio_base'])
        descuento = float(request.POST.get('descuento_aplicado', 0))
        precio_final = precio_base - descuento
        
        Compra.objects.create(
            cliente_id=request.POST['cliente'],
            curso_id=request.POST['curso'],
            fecha_compra=request.POST['fecha_compra'],
            precio_base=precio_base,
            descuento_aplicado=descuento,
            precio_final=precio_final,
            estado=request.POST['estado']
        )
        return redirect('ver_compras')
    
    return render(request, 'admin/crud/compras/agregar.html', {
        'clientes': clientes,
        'cursos': cursos,
        'today': timezone.now().date()
    })

@staff_member_required
def actualizar_compra(request, id):
    # Buscamos la compra
    compra = get_object_or_404(Compra, id=id)
    
    if request.method == 'POST':
        try:
            # 1. Actualizamos la Fecha
            # (Si viene vacía, conservamos la original o ponemos None)
            fecha = request.POST.get('fecha_compra')
            if fecha:
                compra.fecha_compra = fecha
            
            # 2. Actualizamos el Precio Final (Lo que pagó el cliente)
            # No tocamos precio_base ni descuento porque son históricos
            precio = request.POST.get('precio_final')
            if precio:
                compra.precio_final = precio
            
            # 3. Actualizamos el Estado
            compra.estado = request.POST.get('estado')
            
            # Guardamos los cambios
            compra.save()
            return redirect('ver_compras')
            
        except Exception as e:
            # Si hay error, mostramos la página de nuevo con el mensaje
            return render(request, 'admin/crud/compras/editar.html', {
                'compra': compra,
                'error': f"Error al actualizar: {str(e)}"
            })

    return render(request, 'admin/crud/compras/editar.html', {'compra': compra})

def borrar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    if request.method == 'POST':
        compra.delete()
        return redirect('ver_compras')
    return render(request, 'admin/crud/compras/eliminar.html', {'compra': compra})

# ==================== OFERTAS - CRUD COMPLETO ====================
def ver_ofertas(request):
    ofertas = Oferta.objects.all()
    return render(request, 'admin/crud/ofertas/listar.html', {'ofertas': ofertas})

def agregar_oferta(request):
    # 1. Obtenemos todos los cursos para el select
    cursos = Curso.objects.all()

    if request.method == 'POST':
        try:
            # Capturar datos simples
            codigo = request.POST.get('codigo')
            descripcion = request.POST.get('descripcion')
            porcentaje = request.POST.get('porcentaje_descuento')
            fecha_limite = request.POST.get('fecha_limite')
            activo = request.POST.get('activo') == 'on'
            
            # 2. Capturar el ID del curso
            curso_id = request.POST.get('curso')
            curso_seleccionado = None
            if curso_id:
                curso_seleccionado = Curso.objects.get(id=curso_id)

            # 3. Capturar la Imagen
            imagen = request.FILES.get('imagen')

            Oferta.objects.create(
                codigo=codigo,
                descripcion=descripcion,
                porcentaje_descuento=porcentaje,
                fecha_limite=fecha_limite if fecha_limite else None,
                activo=activo,
                curso=curso_seleccionado, # Guardamos la relación
                imagen=imagen             # Guardamos la foto
            )
            return redirect('ver_ofertas')
            
        except Exception as e:
            return render(request, 'admin/crud/ofertas/agregar.html', {
                'error': str(e),
                'cursos': cursos # Devolvemos los cursos si falla
            })

    # Enviamos los cursos al HTML
    return render(request, 'admin/crud/ofertas/agregar.html', {'cursos': cursos})


def actualizar_oferta(request, id):
    oferta = get_object_or_404(Oferta, id=id)
    cursos = Curso.objects.all() # Necesario para el select
    
    if request.method == 'POST':
        try:
            # Actualizar datos de texto
            oferta.codigo = request.POST.get('codigo')
            oferta.descripcion = request.POST.get('descripcion')
            oferta.porcentaje_descuento = request.POST.get('porcentaje_descuento')
            
            # Fecha (si viene vacía, poner None)
            fecha = request.POST.get('fecha_limite')
            oferta.fecha_limite = fecha if fecha else None
            
            # Checkbox
            oferta.activo = request.POST.get('activo') == 'on'
            
            # Relación con Curso
            curso_id = request.POST.get('curso')
            if curso_id:
                oferta.curso = Curso.objects.get(id=curso_id)
            else:
                oferta.curso = None

            # === IMAGEN (Lo más importante) ===
            # Solo la actualizamos si el usuario subió una nueva
            if request.FILES.get('imagen'):
                oferta.imagen = request.FILES.get('imagen')

            oferta.save()
            return redirect('ver_ofertas')
            
        except Exception as e:
            return render(request, 'admin/crud/ofertas/editar.html', {
                'oferta': oferta, 
                'cursos': cursos,
                'error': str(e)
            })

    return render(request, 'admin/crud/ofertas/editar.html', {'oferta': oferta, 'cursos': cursos})

def borrar_oferta(request, id):
    oferta = get_object_or_404(Oferta, id=id)
    if request.method == 'POST':
        oferta.delete()
        return redirect('ver_ofertas')
    return render(request, 'admin/crud/ofertas/eliminar.html', {'oferta': oferta})

# ==================== PAGOS - CRUD COMPLETO ====================
def ver_pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'admin/crud/pagos/listar.html', {'pagos': pagos})

def agregar_pago(request):
    compras = Compra.objects.all()
    
    if request.method == 'POST':
        monto = float(request.POST['monto'])
        iva = monto * 0.16  # Calcular IVA del 16%
        
        Pago.objects.create(
            compra_id=request.POST['compra'],
            fecha_pago=request.POST['fecha_pago'],
            monto=monto,
            iva=iva,
            metodo_pago=request.POST['metodo_pago'],
            referencia=request.POST['referencia'],
            estado_pago=request.POST['estado_pago']
        )
        return redirect('ver_pagos')
    
    return render(request, 'admin/crud/pagos/agregar.html', {
        'compras': compras,
        'now': timezone.now()
    })

def actualizar_pago(request, pago_id):  # Asegúrate que el parámetro sea pago_id
    # Obtener el pago usando el parámetro correcto
    start_time = time.time()
    pago = get_object_or_404(Pago.objects.select_related('compra__cliente', 'compra__curso'), pk=pago_id)
    
    if request.method == 'POST':
        try:
            # IMPORTANTE: Verificar que los campos existan en POST
            # El campo 'compra' ahora está como campo oculto en el template
            compra_id = request.POST.get('compra')
            
            # Actualizar los campos
            pago.monto = request.POST.get('monto', pago.monto)
            pago.fecha_pago = request.POST.get('fecha_pago', pago.fecha_pago)
            pago.metodo_pago = request.POST.get('metodo_pago', pago.metodo_pago)
            pago.estado_pago = request.POST.get('estado', pago.estado_pago)
            pago.referencia_pago = request.POST.get('referencia_pago', pago.referencia_pago)
            pago.banco = request.POST.get('banco', pago.banco)
            pago.observaciones = request.POST.get('observaciones', pago.observaciones)
            
            # Si hay compra_id, actualizarlo
            if compra_id:
                pago.compra_id = compra_id
            
            pago.save()
            messages.success(request, 'Pago actualizado correctamente.')
            return redirect('ver_pagos')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el pago: {str(e)}')
            return render(request, 'admin/crud/pagos/editar.html', {
                'pago': pago,
                'error': str(e)
            })
    
    # GET request - mostrar formulario
    return render(request, 'admin/crud/pagos/editar.html', {
        'pago': pago
    })

def borrar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    if request.method == 'POST':
        pago.delete()
        return redirect('ver_pagos')
    return render(request, 'admin/crud/pagos/eliminar.html', {'pago': pago})

# ==================== TESTIMONIOS - CRUD COMPLETO ====================
def ver_testimonios(request):
    testimonios = Testimonio.objects.all()
    return render(request, 'admin/crud/testimonios/listar.html', {'testimonios': testimonios})

def agregar_testimonio(request):
    # 1. Obtenemos la lista de clientes y cursos
    clientes = Cliente.objects.all()
    cursos = Curso.objects.all()

    if request.method == 'POST':
        try:
            # 2. Capturamos los datos - NOMBRES CORRECTOS
            cliente_id = request.POST.get('cliente')
            contenido = request.POST.get('contenido')  # ✅
            calificacion = request.POST.get('calificacion', 5)
            fecha_creacion = request.POST.get('fecha_creacion')  # ✅
            curso_id = request.POST.get('curso')
            aprobado = 'aprobado' in request.POST
            destacado = 'destacado' in request.POST

            # Validar que se seleccionó un cliente
            if not cliente_id:
                raise ValueError("Debes seleccionar un cliente")

            # 3. Crear el testimonio
            Testimonio.objects.create(
                cliente_id=cliente_id,
                contenido=contenido,  # ✅
                calificacion=calificacion,
                fecha_creacion=fecha_creacion if fecha_creacion else timezone.now().date(),  # ✅
                curso_id=curso_id if curso_id else None,
                aprobado=aprobado,
                destacado=destacado
            )
            return redirect('ver_testimonios')

        except Exception as e:
            return render(request, 'admin/crud/testimonios/agregar.html', {
                'error': str(e),
                'clientes': clientes,
                'cursos': cursos
            })

    # 4. Enviamos datos al template (GET)
    return render(request, 'admin/crud/testimonios/agregar.html', {
        'clientes': clientes,
        'cursos': cursos
    })

def actualizar_testimonio(request, id):
    if request.method == 'POST':
        try:
            testimonio = Testimonio.objects.get(id=id)
            
            # Actualizar campos
            testimonio.contenido = request.POST.get('contenido', '')
            
            if 'fecha_creacion' in request.POST:
                testimonio.fecha_creacion = request.POST['fecha_creacion']
            
            testimonio.calificacion = request.POST.get('calificacion', 5)
            testimonio.curso_id = request.POST.get('curso') or None
            testimonio.aprobado = 'aprobado' in request.POST
            testimonio.destacado = 'destacado' in request.POST
            
            testimonio.save()
            messages.success(request, 'Testimonio actualizado correctamente')
            return redirect('ver_testimonios')
            
        except Testimonio.DoesNotExist:
            messages.error(request, 'El testimonio no existe')
            return redirect('ver_testimonios')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
            return redirect('ver_testimonios')
    
    # GET request
    else:
        try:
            testimonio = Testimonio.objects.get(id=id)
            cursos = Curso.objects.all()
            # CAMBIO AQUÍ: Agregar el path completo de la plantilla
            return render(request, 'admin/crud/testimonios/editar.html', {
                'testimonio': testimonio,
                'cursos': cursos
            })
        except Testimonio.DoesNotExist:
            messages.error(request, 'El testimonio no existe')
            return redirect('ver_testimonios')

def borrar_testimonio(request, id):
    testimonio = get_object_or_404(Testimonio, id=id)
    if request.method == 'POST':
        testimonio.delete()
        return redirect('ver_testimonios')
    return render(request, 'admin/crud/testimonios/eliminar.html', {'testimonio': testimonio})


# ==================== SITIO WEB PÚBLICO ====================
def home(request):
    
    
    """Página principal"""
    cursos_populares = Curso.objects.all()[:6]  # Los 3 primeros cursos
    return render(request, 'website/index.html', {
        'cursos_populares': cursos_populares
    })

def cursos(request):
    """Página de cursos"""
    cursos_lista = Curso.objects.all()
    categorias = Curso.objects.values_list('nivel', flat=True).distinct()
    
    return render(request, 'website/cursos.html', {
        'cursos': cursos_lista,
        'categorias': categorias
    })
    
def detalle_curso(request, id):
    # Buscamos el curso por su ID. Si no existe, muestra error 404.
    curso = get_object_or_404(Curso, id=id)
    
    return render(request, 'website/detalle_curso.html', {
        'curso': curso
    })

def ofertas(request):
    """Vista para ver ofertas públicas"""
    hoy = timezone.now().date()
    
    # Buscamos ofertas que estén ACTIVAS
    # Y que (la fecha límite sea hoy o futuro) O (que no tengan fecha límite)
    ofertas_activas = Oferta.objects.filter(
        activo=True
    ).filter(
        Q(fecha_limite__gte=hoy) | Q(fecha_limite__isnull=True)
    )
    
    return render(request, 'website/ofertas.html', {
        'ofertas': ofertas_activas
    })

def testimonios(request):
    """Página de testimonios"""
    testimonios_lista = Testimonio.objects.all().order_by('-fecha')
    
    # Obtener estadísticas (puedes calcularlas de diferentes maneras)
    total_testimonios = Testimonio.objects.count()
    
    # Calcular porcentaje de clientes satisfechos (ejemplo simplificado)
    total_clientes = Cliente.objects.count()
    clientes_con_testimonios = Testimonio.objects.values('cliente').distinct().count()
    
    if total_clientes > 0:
        total_clientes_satisfechos = min(98, int((clientes_con_testimonios / total_clientes) * 100))
    else:
        total_clientes_satisfechos = 98  # Valor por defecto
    
    return render(request, 'website/testimonios.html', {
        'testimonios': testimonios_lista,
        'total_testimonios': total_testimonios,
        'total_clientes_satisfechos': total_clientes_satisfechos,
    })

# app_Entrenamiento_Canino/views.py

from django.contrib.auth.decorators import login_required

@login_required
def agregar_testimonio_publico(request):
    if request.method == 'POST':
        try:
            contenido = request.POST.get('testimonio')
            rating = request.POST.get('rating') # Obtenemos el valor de las estrellas (1-5)
            
            if hasattr(request.user, 'cliente'):
                Testimonio.objects.create(
                    cliente=request.user.cliente,
                    testimonio=contenido,
                    # Guardamos la calificación (si no viene, ponemos 5 por defecto)
                    calificacion=rating if rating else 5, 
                    fecha=timezone.now()
                )
                messages.success(request, '¡Gracias! Tu testimonio ha sido enviado.')
            else:
                messages.error(request, 'No tienes un perfil de cliente asociado.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('testimonios')

# 2. ACTUALIZAR LA VISTA DE LISTAR (Para calcular los datos reales)
def testimonios(request):
    # Obtener todos los testimonios ordenados por fecha
    lista_testimonios = Testimonio.objects.all().order_by('-fecha_creacion')
    
    # --- CÁLCULOS MATEMÁTICOS REALES ---
    total = lista_testimonios.count()
    
    if total > 0:
        # Calcular promedio (ej: 4.8)
        promedio = lista_testimonios.aggregate(Avg('calificacion'))['calificacion__avg']
        promedio = round(promedio, 1) # Redondear a 1 decimal
        
        # Calcular % de satisfacción (Calificaciones de 4 o 5 estrellas)
        positivos = lista_testimonios.filter(calificacion__gte=4).count()
        porcentaje = int((positivos / total) * 100)
    else:
        promedio = 5.0
        porcentaje = 100

    return render(request, 'website/testimonios.html', {
        'testimonios': lista_testimonios,
        'total_testimonios': total,
        'promedio': promedio,
        'total_clientes_satisfechos': porcentaje
    })
    


@login_required(login_url='/login/')
def comprar_curso(request):
    """Página para comprar curso"""
    curso_id = request.GET.get('id')
    curso = None
    
    if curso_id:
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            curso = None
    
    cursos_lista = Curso.objects.all()
    
    return render(request, 'website/comprar-curso.html', {
        'curso_seleccionado': curso,
        'cursos': cursos_lista
    })

@login_required
def agendar_sesion(request):
    """Página para agendar sesión"""
    # Obtener el cliente asociado al usuario
    try:
        cliente = Cliente.objects.get(correo=request.user.email)
    except Cliente.DoesNotExist:
        messages.error(request, 'No se encontró un perfil de cliente asociado a tu cuenta.')
        return redirect('perfil')
    
    # Obtener compras del cliente
    compras = Compra.objects.filter(cliente=cliente, estado='completado').select_related('curso')
    
    # Obtener perros del cliente
    perros = Perro.objects.filter(cliente=cliente)
    
    # Obtener entrenadores disponibles
    entrenadores = Entrenador.objects.all()
    
    # Obtener citas existentes para evitar conflictos
    citas_existentes = Cita.objects.filter(cliente=cliente).values_list('fecha', 'hora')
    
    context = {
        'cliente': cliente,
        'compras': compras,
        'perros': perros,
        'entrenadores': entrenadores,
        'citas_existentes': list(citas_existentes),
    }
    
    return render(request, 'website/agendar-sesion.html', context)

@login_required
def perfil(request):
    """Página de perfil del usuario"""
    try:
        # Obtener el cliente asociado al usuario
        cliente = Cliente.objects.get(correo=request.user.email)
        
        # Obtener perros del cliente
        perros = Perro.objects.filter(cliente=cliente)
        
        # Obtener compras del cliente
        compras = Compra.objects.filter(cliente=cliente).select_related('curso')
        
        # Obtener pagos del cliente
        pagos = Pago.objects.filter(compra__cliente=cliente).select_related('compra', 'compra__curso')
        
        # Calcular progreso para cada compra
        for compra in compras:
            # Aquí puedes calcular el progreso basado en sesiones completadas, etc.
            compra.progreso = 0  # Por defecto 0%
            
            # Ejemplo: si hay citas completadas
            citas_completadas = Cita.objects.filter(
                cliente=cliente,
                curso=compra.curso,
                estado='completada'
            ).count()
            
            # Supongamos que cada curso tiene 4 sesiones
            if citas_completadas > 0:
                compra.progreso = min(100, (citas_completadas * 100) // 4)
        
    except Cliente.DoesNotExist:
        cliente = None
        perros = []
        compras = []
        pagos = []
        messages.info(request, 'Completa tu perfil de cliente para acceder a todas las funciones.')
    
    context = {
        'cliente': cliente,
        'perros': perros,
        'compras': compras,
        'pagos': pagos,
    }
    
    return render(request, 'website/perfil.html', context)

@login_required
def actualizar_perfil(request):
    """Actualizar información del perfil"""
    if request.method == 'POST':
        try:
            cliente = Cliente.objects.get(correo=request.user.email)
            
            # Actualizar datos del cliente
            cliente.nombre = request.POST.get('nombre')
            cliente.apellido = request.POST.get('apellido')
            cliente.telefono = request.POST.get('telefono')
            cliente.direccion = request.POST.get('direccion')
            cliente.save()
            
            # También actualizar datos del usuario Django
            user = request.user
            user.first_name = request.POST.get('nombre')
            user.last_name = request.POST.get('apellido')
            user.save()
            
            messages.success(request, 'Perfil actualizado correctamente')
            
        except Cliente.DoesNotExist:
            # Crear cliente si no existe
            Cliente.objects.create(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                correo=request.user.email,
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion')
            )
            
            # Actualizar datos del usuario Django
            user = request.user
            user.first_name = request.POST.get('nombre')
            user.last_name = request.POST.get('apellido')
            user.save()
            
            messages.success(request, 'Perfil creado correctamente')
    
    return redirect('perfil')

# ==================== AUTENTICACIÓN ====================
def login_view(request):
    """Vista para iniciar sesión"""
    
    # === CAMBIO 1: Si ya estás dentro, te mando al Perfil (no te saco) ===
    if request.user.is_authenticated:
        return redirect('perfil')
    
    # 2. Inicializar formulario
    form = AuthenticationForm(request) if request.method == 'POST' else AuthenticationForm()
    
    # 3. Manejar POST
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Crear cliente si no existe (Lógica de seguridad)
            if not hasattr(user, 'cliente'):
                try:
                    Cliente.objects.create(
                        usuario=user,
                        nombre=user.first_name or user.username,
                        apellido=user.last_name or 'Pendiente',
                        correo=user.email,
                        telefono='',
                        direccion='',
                    )
                except Exception as e:
                    print(f"Error creando cliente: {e}")
            
            messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
            
            # === CAMBIO 2: Prioridad absoluta a 'perfil' si no hay 'next' ===
            # Verificamos si hay un parámetro 'next', si no, vamos a 'perfil'
            next_url = request.POST.get('next') or request.GET.get('next')
            
            # Si next es 'home' o vacío, forzamos perfil para que veas que entraste
            if not next_url or next_url == 'home':
                next_url = 'perfil'
                
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # 4. Renderizar template
    return render(request, 'website/login.html', {
        'form': form,
        # Quitamos el 'next' del contexto para que no se autrellene con basura
    })
    
def register_view(request):
    """Vista para registrar nuevo usuario"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        # Validaciones
        errors = []
        
        # Verificar si el usuario ya existe
        if User.objects.filter(email=email).exists():
            errors.append('Ya existe una cuenta con este correo electrónico')
        
        if User.objects.filter(username=email).exists():
            errors.append('Ya existe una cuenta con este correo electrónico')
        
        # Verificar contraseñas
        if password1 != password2:
            errors.append('Las contraseñas no coinciden')
        
        if len(password1) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        
        if not errors:
            # Crear usuario
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password1,
                    first_name=nombre,
                    last_name=apellido
                )
                
                # Crear cliente
                Cliente.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    correo=email,
                    telefono=telefono,
                    direccion=direccion
                )
                
                # Autenticar y loguear al usuario
                login(request, user)
                messages.success(request, '¡Cuenta creada exitosamente!')
                
                next_url = request.POST.get('next', 'home')
                return redirect(next_url)
                
            except Exception as e:
                errors.append('Error al crear la cuenta. Intenta nuevamente.')
        
        # Si hay errores, mostrarlos
        for error in errors:
            messages.error(request, error)
    
    return render(request, 'website/login.html', {
        'register': True,
        'next': request.GET.get('next', 'home')
    })

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, '¡Sesión cerrada exitosamente!')
    return redirect('home')

# ==================== ADMIN DASHBOARD ====================
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Dashboard para administradores - VERSIÓN CORREGIDA"""
    from .models import Cliente, Perro, Curso, Compra, Cita, Oferta, Pago, Testimonio
    from django.utils import timezone
    from django.db.models import Count, Sum
    from datetime import date
    
    hoy = date.today()  # Usa date, no timezone para DateField
    inicio_mes = hoy.replace(day=1)
    
    try:
        stats = {
            'clientes': Cliente.objects.count(),
            'perros': Perro.objects.count(),
            'cursos': Curso.objects.count(),
            'compras': Compra.objects.count(),
            'entrenadores': 0,
            'ofertas': Oferta.objects.count(),
            'pagos': Pago.objects.count(),
            'citas': Cita.objects.count(),
            'testimonios': Testimonio.objects.count(),
            
            # CORREGIDO: usa 'precio_final' en lugar de 'monto'
            'ingresos_mes': Compra.objects.filter(
                fecha_compra__gte=inicio_mes
            ).aggregate(total=Sum('precio_final'))['total'] or 0,
            
            'nuevos_clientes': Cliente.objects.filter(
                fecha_registro__gte=inicio_mes
            ).count(),
            
            'compras_pendientes': Compra.objects.filter(
                estado='pendiente'
            ).count(),
            
            # CORREGIDO: para DateField usa solo el campo 'fecha'
            'citas_hoy': Cita.objects.filter(
                fecha=hoy  # ¡SOLO 'fecha', no 'fecha__date'!
            ).count(),
            
            'testimonios_pendientes': Testimonio.objects.filter(
                aprobado=False
            ).count(),
            
            'ofertas_activas': Oferta.objects.filter(
                activa=True
            ).count(),
        }
        
        return render(request, 'admin/crud/dashboard.html', {'stats': stats})
        
    except Exception as e:
        # Vista de emergencia
        print(f"Error en admin_dashboard: {e}")
        return render(request, 'admin/crud/dashboard.html', {
            'stats': {
                'clientes': Cliente.objects.count() if Cliente.objects.exists() else 0,
                'perros': Perro.objects.count() if Perro.objects.exists() else 0,
                'cursos': Curso.objects.count() if Curso.objects.exists() else 0,
                'compras': Compra.objects.count() if Compra.objects.exists() else 0,
                'entrenadores': 0,
                'ofertas': Oferta.objects.count() if Oferta.objects.exists() else 0,
                'pagos': Pago.objects.count() if Pago.objects.exists() else 0,
                'citas': Cita.objects.count() if Cita.objects.exists() else 0,
                'testimonios': Testimonio.objects.count() if Testimonio.objects.exists() else 0,
                'ingresos_mes': 0,
                'nuevos_clientes': 0,
                'compras_pendientes': 0,
                'citas_hoy': 0,
                'testimonios_pendientes': 0,
                'ofertas_activas': 0,
            },
            'error': str(e)
        })
    
@csrf_exempt
@login_required
def procesar_compra(request):
    """Procesar la compra desde AJAX"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            course_id = request.POST.get('course_id')
            dog_name = request.POST.get('dog_name')
            dog_breed = request.POST.get('dog_breed')
            dog_age = request.POST.get('dog_age')
            dog_weight = request.POST.get('dog_weight')
            dog_sex = request.POST.get('dog_sex')
            dog_size = request.POST.get('dog_size')
            dog_behavior = request.POST.get('dog_behavior')
            # dog_experience = request.POST.get('dog_experience') # (Opcional si no lo usas en el modelo)
            payment_method = request.POST.get('payment_method')
            discount_code = request.POST.get('discount_code')
            
            # Buscar el cliente asociado al usuario
            # (Si usaste mi corrección anterior de login, esto es más seguro así:)
            if hasattr(request.user, 'cliente'):
                cliente = request.user.cliente
            else:
                # Fallback por si acaso
                cliente, created = Cliente.objects.get_or_create(
                    correo=request.user.email,
                    defaults={
                        'nombre': request.user.first_name or 'Cliente',
                        'apellido': request.user.last_name or '',
                        'telefono': '',
                        'direccion': '',
                        'usuario': request.user
                    }
                )
            
            # Buscar el curso
            curso = Curso.objects.get(id=course_id)
            
            # --- CÁLCULOS MONETARIOS CORREGIDOS ---
            precio_base = curso.precio # Esto ya es un Decimal desde la BD
            descuento_aplicado = Decimal('0.00') # Inicializar como Decimal
            
            # Aplicar descuento si hay código válido
            if discount_code:
                try:
                    oferta = Oferta.objects.get(codigo=discount_code)
                    
                    # 2. CORRECCIÓN AQUÍ: Usar Decimal('100') para la división
                    # Asumiendo que porcentaje_descuento es un número entero o decimal en tu modelo
                    descuento_aplicado = (precio_base * oferta.porcentaje_descuento) / Decimal('100')
                    
                except Oferta.DoesNotExist:
                    pass
            
            # Restar decimales es seguro
            precio_final = precio_base - descuento_aplicado
            
            # Crear compra
            compra = Compra.objects.create(
                cliente=cliente,
                curso=curso,
                fecha_compra=timezone.now().date(),
                precio_base=precio_base,
                descuento_aplicado=descuento_aplicado,
                precio_final=precio_final,
                estado='pendiente'
            )
            
            # Crear perro si no existe
            # Convertimos edad y peso a números por seguridad
            try:
                age_int = int(dog_age)
            except (ValueError, TypeError):
                age_int = 0
                
            try:
                weight_float = float(dog_weight)
            except (ValueError, TypeError):
                weight_float = 0.0

            perro, created = Perro.objects.get_or_create(
                cliente=cliente,
                nombre=dog_name,
                defaults={
                    'raza': dog_breed,
                    'edad': age_int,
                    'sexo': dog_sex,
                    # Asegúrate de agregar los otros campos si tu modelo los tiene
                    'peso': weight_float, 
                    'tamano': dog_size,
                    'comportamiento': dog_behavior
                }
            )
            
            # Crear pago
            Pago.objects.create(
                compra=compra,
                fecha_pago=timezone.now(),
                monto=precio_final,
                
                # 3. CORRECCIÓN AQUÍ: Usar Decimal('0.16') en lugar de 0.16
                iva=precio_final * Decimal('0.16'),
                
                metodo_pago=payment_method,
                referencia=f"PAY-{compra.id}-{timezone.now().strftime('%Y%m%d')}",
                estado_pago='pendiente' # O 'completado' si quieres simular éxito inmediato
            )
            
            # Actualizar estado de compra
            compra.estado = 'completado'
            compra.save()
            
            return JsonResponse({
                'success': True,
                'compra_id': compra.id,
                'message': 'Compra procesada exitosamente'
            })
            
        except Exception as e:
            # Imprimir el error en la terminal para que puedas verlo
            print(f"ERROR EN COMPRA: {e}") 
            return JsonResponse({
                'success': False,
                'error': f"Ocurrió un error: {str(e)}"
            })

    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })
    
@csrf_exempt
@login_required
def procesar_cita(request):
    """Procesar la cita desde AJAX"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            curso_id = request.POST.get('curso_id')
            entrenador_id = request.POST.get('entrenador_id')
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')
            perro_id = request.POST.get('perro_id')
            notas = request.POST.get('notas', '')
            
            # Buscar el cliente asociado al usuario
            try:
                cliente = Cliente.objects.get(correo=request.user.email)
            except Cliente.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'No se encontró un perfil de cliente asociado a tu cuenta.'
                })
            
            # Buscar el curso
            try:
                curso = Curso.objects.get(id=curso_id)
            except Curso.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'El curso seleccionado no existe.'
                })
            
            # Buscar el entrenador
            try:
                entrenador = Entrenador.objects.get(id=entrenador_id)
            except Entrenador.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'El entrenador seleccionado no existe.'
                })
            
            # Buscar el perro si se especificó
            perro = None
            if perro_id:
                try:
                    perro = Perro.objects.get(id=perro_id, cliente=cliente)
                except Perro.DoesNotExist:
                    pass
            
            # Verificar si ya existe una cita en esa fecha y hora
            cita_existente = Cita.objects.filter(
                entrenador=entrenador,
                fecha=fecha,
                hora=hora
            ).exists()
            
            if cita_existente:
                return JsonResponse({
                    'success': False,
                    'error': 'El entrenador ya tiene una cita programada en ese horario.'
                })
            
            # Crear la cita
            cita = Cita.objects.create(
                cliente=cliente,
                curso=curso,
                entrenador=entrenador,
                perro=perro,
                fecha=fecha,
                hora=hora,
                notas=notas,
                estado=''
            )
            
            # Aquí podrías agregar:
            # 1. Envío de email de confirmación
            # 2. Notificación al entrenador
            # 3. Agregar a calendario del cliente
            
            return JsonResponse({
                'success': True,
                'cita_id': cita.id,
                'message': 'Cita agendada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })

def suscribir_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Validación básica
        if email:
            # Verificar si el email ya existe
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(
                    email=email,
                    fecha_suscripcion=timezone.now(),
                    activo=True
                )
                messages.success(request, '¡Te has suscrito exitosamente a nuestro newsletter!')
            else:
                messages.info(request, 'Este email ya está suscrito a nuestro newsletter.')
        else:
            messages.error(request, 'Por favor ingresa un email válido.')
    
    # Redirigir a la página anterior o al home
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# Decorador personalizado para verificar staff
def staff_required(view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url or '/login/'
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

# Decorador para superusuarios
def superuser_required(view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url or '/login/'
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


@staff_member_required
def admin_dashboard(request):
    """Panel de control principal del administrador"""
    
    # 1. Calculamos los conteos generales
    # El método .count() es muy rápido y eficiente
    stats = {
        'clientes': Cliente.objects.count(),
        'perros': Perro.objects.count(),
        'cursos': Curso.objects.count(),
        'compras': Compra.objects.count(),
        'entrenadores': Entrenador.objects.count(),
        'ofertas': Oferta.objects.count(),
        'pagos': Pago.objects.count(),
        'citas': Cita.objects.count(),
        'testimonios': Testimonio.objects.count(),
        
        # 2. Datos para la sección "Estadísticas Recientes"
        # Por ahora pondremos conteos simples o 0 para que no dé error
        'ingresos_mes': 0,  # Aquí podrías sumar los pagos del mes si quisieras
        'nuevos_clientes': Cliente.objects.count(), # Total por ahora
        'compras_pendientes': 0,
        'citas_hoy': 0,
        'testimonios_pendientes': 0,
        'ofertas_activas': Oferta.objects.count(),
    }
    
    # 3. Lista vacía de actividades para que no falle el bucle final
    actividades = []

    # 4. Enviamos todo al HTML
    return render(request, 'admin/crud/dashboard.html', {
        'stats': stats, 
        'actividades': actividades
    })
    
@superuser_required
def superadmin_settings(request):
    # Solo accesible para superusuarios
    return render(request, 'admin/superadmin_settings.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            # 1. Guardar el Usuario de Django (Login)
            user = form.save(commit=False)
            user.first_name = request.POST.get('nombre')
            user.last_name = request.POST.get('apellido')
            user.email = request.POST.get('email')
            user.save()
            
            # 2. CREAR EL CLIENTE
            Cliente.objects.create(
                usuario=user,          # <--- AHORA SÍ podemos enlazarlo
                nombre=user.first_name,
                apellido=user.last_name,
                correo=user.email,
                telefono="",
                direccion=""
            )
            
            # 3. Loguear y redirigir
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'website/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

@login_required
def password_changes(request):
    """Vista simple para cambiar contraseña"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'website/password_changes.html', {'form': form})

# app_Entrenamiento_Canino/views.py
def limpiar_sesion(request):
    """Vista especial para desarrollo - limpia TODO"""
    from django.contrib.auth import logout
    
    if request.user.is_authenticated:
        logout(request)
    
    request.session.flush()  # Elimina toda la sesión
    
    # Respuesta simple
    return HttpResponse("""
    <html>
    <body style="background: black; color: lime; padding: 50px; font-family: monospace;">
        <h1>✅ SESIÓN LIMPIADA</h1>
        <p>Todo ha sido borrado. Ahora puedes:</p>
        <ul>
            <li><a href="/" style="color: cyan;">Ir al Home</a></li>
            <li><a href="/login/" style="color: cyan;">Ir al Login</a></li>
        </ul>
        <script>
            // Redirigir automáticamente después de 2 segundos
            setTimeout(function() {
                window.location.href = '/';
            }, 2000);
        </script>
    </body>
    </html>
    """)
    
# Decorador para admin
def admin_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))

# Vista pública de ofertas
def ofertas_publicas(request):
    """Vista pública de ofertas"""
    from .models import Oferta
    ofertas = Oferta.objects.filter(activa=True).order_by('-fecha_creacion')
    return render(request, 'website/ofertas.html', {'ofertas': ofertas})

# Vista admin de ofertas
@admin_required
def ver_ofertas_admin(request):
    """Vista de ofertas para el admin"""
    from .models import Oferta
    ofertas = Oferta.objects.all().order_by('-fecha_creacion')
    return render(request, 'admin/crud/ofertas/listar.html', {'ofertas': ofertas})

# Vista pública de testimonios
def testimonios_publicos(request):
    """Vista pública de testimonios"""
    from .models import Testimonio
    testimonios = Testimonio.objects.filter(aprobado=True).order_by('-fecha_creacion')
    return render(request, 'website/testimonios.html', {'testimonios': testimonios})

# Vista admin de testimonios
@admin_required
def ver_testimonios_admin(request):
    """Vista de testimonios para el admin"""
    from .models import Testimonio
    testimonios = Testimonio.objects.all().order_by('-fecha_creacion')
    return render(request, 'admin/crud/testimonios/listar.html', {'testimonios': testimonios})
    
@staff_member_required # Esto protege la vista para que solo admins entren
def agregar_perro_admin(request):
    # Obtener todos los clientes para el <select> del formulario
    clientes = Cliente.objects.all() 

    if request.method == 'POST':
        # Recibir datos del formulario HTML
        nombre = request.POST.get('nombre')
        raza = request.POST.get('raza')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        peso = request.POST.get('peso')
        tamano = request.POST.get('tamaño') # Ojo con la ñ en el name del HTML
        comportamiento = request.POST.get('comportamiento')
        cliente_id = request.POST.get('cliente')

        # Buscar la instancia del cliente seleccionado
        cliente_obj = None
        if cliente_id:
            cliente_obj = get_object_or_404(Cliente, id=cliente_id)

        # Crear el perro
        Perro.objects.create(
            nombre=nombre,
            raza=raza,
            edad=edad,
            sexo=sexo,
            peso=peso if peso else 0, # Manejo de vacío
            tamano=tamano,            # Asegúrate que tu modelo tenga este campo (o 'tamanio')
            comportamiento=comportamiento,
            cliente=cliente_obj       # Aquí asignamos el dueño
        )
        
        # AQUÍ ESTÁ LA CLAVE: Redirigir a la lista de administración
        return redirect('ver_perros')

    # Si es GET, mostramos el formulario
    return render(request, 'admin/crud/perros/agregar.html', {'clientes': clientes})