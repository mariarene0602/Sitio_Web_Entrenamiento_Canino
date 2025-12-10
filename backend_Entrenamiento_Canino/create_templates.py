# create_templates.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'app_Entrenamiento_Canino')
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates', 'admin')

# Crear directorios si no existen
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Contenido para login.html
login_content = '''{% extends "admin/login.html" %}
{% load static %}

{% block extrastyle %}
{{ block.super }}
<style>
    body.login {
        background: linear-gradient(135deg, #8b6b4d 0%, #2c3e50 100%) !important;
        font-family: 'Montserrat', sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
    }
    
    #container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        width: 100%;
        max-width: 450px;
        padding: 0 !important;
        border: none;
    }
    
    #header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
        padding: 30px !important;
        text-align: center;
        border-radius: 0 !important;
    }
    
    #branding h1 {
        color: white !important;
        font-family: 'Playfair Display', serif;
        font-size: 2rem !important;
        margin: 0 !important;
    }
    
    #content {
        padding: 40px !important;
    }
    
    .form-row {
        margin-bottom: 20px !important;
    }
    
    .form-row label {
        display: block;
        margin-bottom: 8px;
        color: #333;
        font-weight: 600;
    }
    
    input[type="text"],
    input[type="password"] {
        width: 100% !important;
        padding: 12px 15px !important;
        border: 2px solid #ddd !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }
    
    .submit-row {
        text-align: center !important;
        padding: 0 !important;
        margin-top: 30px !important;
    }
    
    .submit-row input {
        background: linear-gradient(135deg, #8b6b4d 0%, #a07d5a 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        padding: 15px !important;
        width: 100% !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        cursor: pointer !important;
    }
    
    .submit-row input:hover {
        background: linear-gradient(135deg, #7a5c42 0%, #8b6b4d 100%) !important;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
{% endblock %}

{% block branding %}
<div style="text-align: center;">
    <div style="font-size: 2.5rem; color: white; margin-bottom: 10px;">
        <i class="fas fa-paw"></i>
    </div>
    <h1 style="color: white; margin: 0; font-family: 'Playfair Display', serif;">
        CANIS ACADEMIA
    </h1>
    <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">
        Panel de Administración
    </p>
</div>
{% endblock %}
'''

# Contenido para base_site.html
base_site_content = '''{% extends "admin/base.html" %}
{% load static %}

{% block title %}{{ title }} | CANIS ACADEMIA Admin{% endblock %}

{% block branding %}
<h1 id="site-name">
    <a href="{% url 'admin:index' %}" style="color: white; text-decoration: none;">
        <i class="fas fa-paw"></i> CANIS ACADEMIA - Admin Panel
    </a>
</h1>
{% endblock %}

{% block extrastyle %}
<style>
    #header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
    }
    
    #branding h1 {
        color: white !important;
        font-family: 'Playfair Display', serif;
    }
    
    .module h2, .module caption {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
    }
    
    .button, input[type="submit"] {
        background: #8b6b4d !important;
        border: none !important;
        border-radius: 6px !important;
    }
    
    .button:hover, input[type="submit"]:hover {
        background: #7a5c42 !important;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{% endblock %}
'''

# Escribir los archivos
login_path = os.path.join(TEMPLATES_DIR, 'login.html')
base_site_path = os.path.join(TEMPLATES_DIR, 'base_site.html')

with open(login_path, 'w', encoding='utf-8') as f:
    f.write(login_content)

with open(base_site_path, 'w', encoding='utf-8') as f:
    f.write(base_site_content)

print(f"✅ Templates creados en: {TEMPLATES_DIR}")
print("1. login.html")
print("2. base_site.html")
print("\nReinicia el servidor Django para ver los cambios.")