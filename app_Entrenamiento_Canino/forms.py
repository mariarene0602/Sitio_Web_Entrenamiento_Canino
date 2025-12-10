# app_Entrenamiento_Canino/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Perro, Entrenador, Curso, Oferta, Cita, Compra, Pago, Testimonio, Newsletter

class TestimonioForm(forms.ModelForm):
    class Meta:
        model = Testimonio
        fields = ['cliente', 'contenido', 'calificacion', 'curso', 'aprobado', 'destacado']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si quieres personalizar el queryset de clientes
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre')