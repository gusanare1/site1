from django import forms
from django.forms import ModelForm
from .models import Carro, Color, Marca, Modelo, Ciudad, Provincia, Persona

class PersonaForm(ModelForm):
	exclude = ('id')
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CarroForm(ModelForm):
	fields = ('placa','imagen',)

	provincia = forms.ModelChoiceField(queryset = Provincia.objects.all(), empty_label=None)
	color = forms.ModelChoiceField(queryset = Color.objects.all(), empty_label=None)
	ciudad = forms.ModelChoiceField(queryset = Ciudad.objects.all())
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.all())
	marca = forms.ModelChoiceField(queryset = Marca.objects.all(), empty_label=None)
	usuario = forms.CharField(disabled=True, required=False)

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
		exclude = ('id','esta_inspeccionado','inspeccion', 'imagen_nombre',
		#'color','marca','modelo','provincia','ciudad'
		)
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
	cedula = forms.CharField(max_length=10, label='Cedula')
	celular = forms.IntegerField( label='Celular')
	ciudad = forms.ModelChoiceField(queryset = Ciudad.objects.all())
	password1=forms.CharField(max_length=30, label='Password', widget=forms.PasswordInput)
	password2=forms.CharField(max_length=20, label='Password Again', widget=forms.PasswordInput)
	def clean(self):
	    cd = self.cleaned_data
	    username = cd.get('username')
	    try:
	        if Persona.objects.get(username = username):
	            self.add_error('username','Usuario existente')
	    except:
	        pass
	    first_name = cd.get('first_name')
	    last_name = cd.get('last_name')
	    cedula = cd.get('cedula')
	    patron ="\W" #CARACTERES NO ALFANUMERICOS (posible danino
	    if re.search(patron, first_name):
	        self.add_error('first_name','Solo se aceptan letras')
	    if re.search(patron, last_name):
	        self.add_error('last_name','Solo se aceptan letras')

	    valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
	    suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
	    veri = 10 - (suma - (10 * (suma // 10)))#PYTHON3 // es division(cociente)
	    if not (int(cedula[9]) == int(str(veri)[-1:])):
	        self.add_error('cedula',"La cedula no es valida")

	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','celular','ciudad',)

class BusquedaForm(forms.Form):
	anio = forms.IntegerField( label='Año inicio busqueda')
	tiempo = forms.IntegerField( label='Buscar carros hasta ____ años despues')
	precio = forms.FloatField(label="Precio Maximo")
	ciudad = forms.ModelChoiceField(queryset = Ciudad.objects.all())
	marca = forms.ModelChoiceField(queryset = Marca.objects.all())
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.all())

	def clean(self):
		cd = self.cleaned_data
		marca = cd.get("marca")
		modelo = cd.get("modelo")
		anio = cd.get("anio")
		precio = cd.get("precio")
		if anio<1000:
			return ValidateError("Carro antiguo")

		return cd

class LoginForm(forms.Form):
    attrs = {"type": "password"}
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32,widget=forms.TextInput(attrs=attrs))