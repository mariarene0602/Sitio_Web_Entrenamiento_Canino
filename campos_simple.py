# campos_simple.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_Entrenamiento_Canino.settings')
import django
django.setup()

from app_Entrenamiento_Canino.models import Testimonio

print("LISTA DE CAMPOS:")
for f in Testimonio._meta.fields:
    print(f.name)