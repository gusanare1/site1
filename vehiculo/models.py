
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Provincia(models.Model):
	nombre = models.CharField(max_length=30)
	
	def __str__(self):
		return self.nombre
		
class Ciudad(models.Model):
	nombre = models.CharField(max_length=30)
	provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.nombre

class Marca(models.Model):
	nombre = models.CharField(max_length=30)
	
	def __str__(self):
		return self.nombre
		
class Modelo(models.Model):
	nombre = models.CharField(max_length=30)
	marca = models.ForeignKey(Marca, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.nombre

class Color(models.Model):
	nombre = models.CharField(max_length=30)
		
	def __str__(self):
		return self.nombre
	
#DATOS SECUNDARIOS
class Persona(models.Model):
	#user = models.OneToOneField(User, on_delete=models.CASCADE, default=-1)
	cedula = models.CharField(max_length=10, primary_key=True)
	username = models.CharField(max_length=30,default="", unique=True)
	correo = models.EmailField(max_length=70, blank=True)
	def __str__(self):
		return self.username+" "+self.cedula

class Ant(models.Model):
	
	motor = models.CharField(max_length=50)
	chasis = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre
		
from django.contrib.auth.models import User

class Carro(models.Model):
	placa = models.CharField(max_length=10, default="AAA-0000", help_text = "Ejemplo: XXX-0XXX")
	anio = models.IntegerField(default = 2000)
	precio = models.FloatField(default = 0.00)
	esta_inspeccionado = models.BooleanField(default = False)
	color = models.ForeignKey(Color, on_delete = models.DO_NOTHING, default = -1)
	marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING,default = -1)
	modelo = models.ForeignKey(Modelo, on_delete = models.DO_NOTHING, default = -1)
	provincia = models.ForeignKey(Provincia, on_delete = models.DO_NOTHING, default = -1)
	ciudad = models.ForeignKey(Ciudad, on_delete = models.DO_NOTHING, default = -1)
	#dueno = models.CharField(max_length=100, default="No")
	usuario = models.ForeignKey(User, on_delete = models.DO_NOTHING, default=-1)
	#inspeccion = models.OneToOneField(Inspeccion, on_delete=models.CASCADE, default=-1)
	#enreadonly_fields = ('',)
	#ant = models.ForeignKey(Ant, on_delete = models.CASCADE, default=-1)
	imagen = models.ImageField( default = 'no_image.jpg')
	def __str__(self):
		if self.esta_inspeccionado:
			tex_ = "(Esta Inspeccionado)"
		else:
			tex_ = "(No esta inspeccionado)"
		return self.modelo.nombre+" "+self.placa+" "+tex_
	
	
class Inspeccion(models.Model):
	carro = models.ForeignKey(Carro, on_delete=models.DO_NOTHING, default = -1)
	choque = models.CharField(max_length=20)
	observacion = models.CharField(max_length=200)
	def __str__(self):
		return self.choque