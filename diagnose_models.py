# diagnose_models.py (en la raíz de tu proyecto)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_Entrenamiento_Canino.settings')
django.setup()

from app_Entrenamiento_Canino.models import Testimonio

print("=== DIAGNÓSTICO DEL MODELO TESTIMONIO ===")
print(f"Nombre del modelo: {Testimonio.__name__}")
print("\nCampos disponibles:")

try:
    for field in Testimonio._meta.get_fields():
        print(f"  - {field.name} ({field.__class__.__name__})")
except Exception as e:
    print(f"Error: {e}")

print("\nCampos locales (no relaciones):")
for field in Testimonio._meta.fields:
    print(f"  - {field.name} ({field.get_internal_type()})")