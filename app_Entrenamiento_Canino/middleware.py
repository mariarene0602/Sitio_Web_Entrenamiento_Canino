# app_Entrenamiento_Canino/middleware.py
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # URLs donde SIEMPRE forzar logout (páginas públicas)
        public_urls = [
            '/',  # home
            '/login/',      # Tu login personalizado (NO admin)
            '/register/',
            '/cursos/',
            '/ofertas/',
            '/testimonios/',
            '/comprar/',
        ]
        
        # URLs que NO deben forzar logout (admin y otras)
        exclude_urls = [
            '/admin/',      # Todo el admin
            '/admin/login/', # Login del Django Admin específicamente
            '/admin/logout/',
            '/admin_dashboard/',  # Tu dashboard personalizado
            '/perfil/',     # Páginas de usuario autenticado
            '/logout/',     # La acción de logout
        ]
        
        # Verificar si la URL actual está en la lista de exclusión
        is_excluded = any(request.path.startswith(url) for url in exclude_urls)
        
        # Solo forzar logout si:
        # 1. NO está en la lista de exclusión
        # 2. Está en la lista de URLs públicas
        # 3. El usuario está autenticado
        if not is_excluded and any(request.path.startswith(url) for url in public_urls):
            if request.user.is_authenticated:
                logout(request)
                request.session.flush()  # Limpia toda la sesión
                print(f"🔐 Middleware: Sesión cerrada en {request.path}")
        
        response = self.get_response(request)
        return response