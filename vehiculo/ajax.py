from django.http import JsonResponse

from .models import Ciudad, Provincia, Marca, Modelo, Carro

def get_ciudades(request):
	provincia_id = request.GET.get('provincia_id')
	ciudades = Ciudad.objects.none()
	options = ''
	if provincia_id:
		ciudades = Ciudad.objects.filter(provincia_id=provincia_id)
	for ciudad in ciudades:
		options += '<option value="%s">%s</option>' %(ciudad.pk, ciudad.nombre)
	response={}
	response['ciudades'] = options
	return JsonResponse(response)
	
def get_modelos(request):
	marca_id = request.GET.get('marca_id')
	modelos = Modelo.objects.none()
	options = ''
	if marca_id:
		modelos = Modelo.objects.filter(marca_id=marca_id)
	for modelo in modelos:
		options += '<option value="%s">%s</option>' %(modelo.pk, modelo.nombre)
	response={}
	response['modelos'] = options
	return JsonResponse(response)
	
def get_cars_by_model_name(request):
	nombre = request.GET.get('nombre')
	carros = Carro.objects.none()
	options = ''
	nombre = nombre_.replace('%20',' ')
	if nombre:
		#modelo_id = Modelo.objects.filter(nombre__contains=nombre)
		carros = Carro.objects.filter(modelo__nombre__contains=nombre)
	for carro in carros:
		options += "<li> <a href='%s/'> %s</li>" %(carro.pk, carro.placa+"-"+carro.provincia.nombre)
	response={}
	response['carros'] = options
	return JsonResponse(response)
	
	
def get_model_name(request):
	nombre = request.GET.get('nombre')
	modelos = Modelo.objects.none()
	options = ''
	if nombre:
		#modelos = Modelo.objects.filter(nombre__contains=nombre)
		modelos = Carro.objects.filter(modelo__nombre__contains = nombre)
	for modelo_carro in modelos:
		print(modelo_carro)
		options += '<option value="%s">' %(modelo_carro.modelo.nombre)
	response={}
	response['modelos'] = options
	return JsonResponse(response)