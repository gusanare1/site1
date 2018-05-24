from django import forms
from django.forms import ModelForm
from .models import Carro, Color, Marca, Modelo, Ciudad, Provincia, Persona

class PersonaForm(ModelForm):
	exclude = ('id')

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CarroForm(ModelForm):
	fields = ('placa', )
	provincia = forms.ModelChoiceField(queryset = Provincia.objects.all(), empty_label=None)
	color = forms.ModelChoiceField(queryset = Color.objects.all(), empty_label=None)
	ciudad = forms.ModelChoiceField(queryset = Ciudad.objects.all())
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.all())
	marca = forms.ModelChoiceField(queryset = Marca.objects.all(), empty_label=None)
	usuario = forms.CharField(disabled=True, required=False)
	import re
	def clean(self):
		cd = self.cleaned_data
		marca = cd.get('marca')
		anio = cd.get("anio")
		placa = cd.get('placa')
		
		if not re.search("[a-zA-Z]{3}[ -]?\d{4}", placa):
			self.add_error('placa', "La placa no es correcta (XXX-0XXX)")
			
		if anio<1900:
			#raise forms.ValidationError("Carro")
			self.add_error('anio','El carro es demasiado viejo')
		return cd
		
	class Meta:
		#fields = ('anio','precio','esta_inspeccionado', 'provincia', 'ciudad', 'dueno')
		exclude = ('id','esta_inspeccionado','inspeccion',)
		model = Carro
		readonly_fields = ('usuario',)
	def __init__(self, *args, **kwargs):
		super(CarroForm, self).__init__(*args, **kwargs)
		self.fields['provincia'].empty_label = None
		
class ColorForm(ModelForm):
	exclude = ('id',)
class ModeloForm(ModelForm):
	exclude = ('id',)
class ProvinciaForm(ModelForm):
	exclude = ('id',)
class CiudadForm(ModelForm):
	exclude = ('id',)
class MarcaForm(forms.Form):
	marca = forms.ModelChoiceField(queryset = Marca.objects.all())
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.all())
	
class SignUpForm(UserCreationForm):
	username = forms.CharField(  max_length=32, label='Username')
	first_name = forms.CharField(max_length=32, label='First name')
	last_name=forms.CharField( max_length=32, label='Last name')
	email=forms.EmailField(max_length=64, help_text='Enter a valid email address')
	cedula = forms.IntegerField( label='Cedula')
	celular = forms.IntegerField( label='Celular')
	ciudad = forms.CharField(max_length=10, label='Ciudad')
	password1=forms.CharField(max_length=30, label='Password')
	password2=forms.CharField(max_length=20, label='Password Again')
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','celular','ciudad',)
		
class BusquedaForm(ModelForm):
	marca = forms.ModelChoiceField(queryset = Marca.objects.all())
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.all())
	anio = forms.IntegerField( label='Year')
	
	def clean(self):
		cd = self.cleaned_data
		marca = cd.get("marca")
		modelo = cd.get("modelo")
		anio = cd.get("anio")
		
		if anio<1900:
			return ValidateError("Carro antiguo")
		
		return cd