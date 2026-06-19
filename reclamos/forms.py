# Asegúrate de que este nombre sea exactamente "ReclamoForm"
from django import forms
from .models import Reclamo

class ReclamoForm(forms.ModelForm): # <--- Este nombre debe coincidir
    class Meta:
        model = Reclamo
        fields = ['tipo', 'titulo', 'descripcion']