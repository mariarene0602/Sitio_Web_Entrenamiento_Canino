# check_templates.py
import os
import django
from django.conf import settings
from django.template.loader import get_template

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_Entrenamiento_Canino.settings')
django.setup()

# Verificar templates
templates_to_check = ['admin/login.html', 'admin/base_site.html']

for template_name in templates_to_check:
    try:
        template = get_template(template_name)
        print(f"✅ ENCONTRADO: {template_name}")
        print(f"   Ruta: {template.origin.name}")
    except Exception as e:
        print(f"❌ NO ENCONTRADO: {template_name}")
        print(f"   Error: {e}")

# Verificar directorios de templates
print("\n📁 Directorios de templates configurados:")
for template_dir in settings.TEMPLATES[0]['DIRS']:
    print(f"   - {template_dir}")
    if os.path.exists(template_dir):
        print(f"     ✅ Existe")
        # Listar archivos
        for root, dirs, files in os.walk(template_dir):
            level = root.replace(template_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')
    else:
        print(f"     ❌ No existe")