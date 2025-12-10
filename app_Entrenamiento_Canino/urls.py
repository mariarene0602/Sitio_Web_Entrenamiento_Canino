# app_Entrenamiento_Canino/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('suscribir-newsletter/', views.suscribir_newsletter, name='suscribir_newsletter'),
    
    # ==================== URLs PÚBLICAS ====================
    # Estas se quedan igual porque son las que ve el cliente
    path('', views.home, name='home'),
    path('cursos/', views.cursos, name='cursos'), 
    path('curso/<int:id>/', views.detalle_curso, name='detalle_curso'),
    path('ofertas-publicas/', views.ofertas, name='ofertas'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('testimonios/nuevo/', views.agregar_testimonio_publico, name='agregar_testimonio_publico'),
    path('comprar/', views.comprar_curso, name='comprar_curso'),
    
    # ... (Tus rutas de perfil y auth siguen igual) ...
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('perros/agregar/', views.agregar_perro, name='agregar_perro'),
    path('perros/borrar/<int:id>/', views.borrar_perro, name='borrar_perro'),
    path('agendar-sesion/', views.agendar_sesion, name='agendar_sesion'),
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ... (Tus rutas de password reset siguen igual) ...
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='website/password_reset.html', email_template_name='website/password_reset_email.html', subject_template_name='website/password_reset_subject.txt', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='website/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='website/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='website/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='website/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='website/password_change_done.html'), name='password_change_done'),
    
    path('procesar-compra/', views.procesar_compra, name='procesar_compra'),
    
    # ==================== URLs DEL ADMIN ====================
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.inicio_entrenamiento_canino, name='inicio'), # OJO: Esto también choca con el home, pero está abajo.
    
    # Clientes
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/borrar/<int:id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # Perros
    path('perros-admin/', views.ver_perros, name='ver_perros'), # Recomendado cambiar para evitar choque con perfil
    path('gestion/perros/agregar/', views.agregar_perro_admin, name='agregar_perro_admin'),
    path('perros-admin/actualizar/<int:id>/', views.actualizar_perro, name='actualizar_perro'),
    path('perros-admin/borrar/<int:id>/', views.borrar_perro, name='borrar_perro_admin'),
    
    # Entrenadores
    path('entrenadores/', views.ver_entrenadores, name='ver_entrenadores'),
    path('entrenadores/agregar/', views.agregar_entrenador, name='agregar_entrenador'),
    path('entrenadores/actualizar/<int:id>/', views.actualizar_entrenador, name='actualizar_entrenador'),
    path('entrenadores/borrar/<int:id>/', views.borrar_entrenador, name='borrar_entrenador'),
    
    # === AQUÍ ESTABA EL ERROR PRINCIPAL (Cursos) ===
    # Le agregamos un prefijo 'gestion-' o 'admin-' para diferenciarlas
    path('gestion/cursos/', views.ver_cursos, name='ver_cursos'),       # <--- CAMBIO AQUÍ
    path('gestion/cursos/agregar/', views.agregar_curso, name='agregar_curso'),
    path('gestion/cursos/actualizar/<int:id>/', views.actualizar_curso, name='actualizar_curso'),
    path('gestion/cursos/borrar/<int:id>/', views.borrar_curso, name='borrar_curso'),
    
    # Ofertas
    path('ofertas/', views.ver_ofertas, name='ver_ofertas'),
    path('ofertas/agregar/', views.agregar_oferta, name='agregar_oferta'),
    path('ofertas/actualizar/<int:id>/', views.actualizar_oferta, name='actualizar_oferta'),
    path('ofertas/borrar/<int:id>/', views.borrar_oferta, name='borrar_oferta'),
    
    # Citas
    path('citas/', views.ver_citas, name='ver_citas'),
    path('citas/agregar/', views.agregar_cita, name='agregar_cita'),
    path('citas/actualizar/<int:id>/', views.actualizar_cita, name='actualizar_cita'),
    path('citas/borrar/<int:id>/', views.borrar_cita, name='borrar_cita'),
    
    # Compras
    path('compras/', views.ver_compras, name='ver_compras'),
    path('compras/agregar/', views.agregar_compra, name='agregar_compra'),
    path('compras/actualizar/<int:id>/', views.actualizar_compra, name='actualizar_compra'),
    path('compras/borrar/<int:id>/', views.borrar_compra, name='borrar_compra'),
    
    # Pagos
    path('pagos/', views.ver_pagos, name='ver_pagos'),
    path('pagos/agregar/', views.agregar_pago, name='agregar_pago'),
    path('pagos/actualizar/<int:pago_id>/', views.actualizar_pago, name='actualizar_pago'),
    path('pagos/borrar/<int:id>/', views.borrar_pago, name='borrar_pago'),
    
    # === AQUÍ ESTABA EL OTRO ERROR (Testimonios) ===
    path('gestion/testimonios/', views.ver_testimonios, name='ver_testimonios'),  # <--- CAMBIO AQUÍ
    path('gestion/testimonios/agregar/', views.agregar_testimonio, name='agregar_testimonio'),
    path('gestion/testimonios/actualizar/<int:id>/', views.actualizar_testimonio, name='actualizar_testimonio'),
    path('gestion/testimonios/borrar/<int:id>/', views.borrar_testimonio, name='borrar_testimonio'),
]