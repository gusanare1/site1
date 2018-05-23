from django.shortcuts import render,redirect,get_object_or_404
from .forms import CarroForm, SignUpForm, BusquedaForm
from .models import Color, Marca, Modelo, Provincia, Ciudad, Carro, Inspeccion, Persona
# Create your views here.
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib import auth
from django.contrib.auth.models import User
'''
def handler404(request, exception, template_name='vehiculo/404.html'):
    response = render_to_response('vehiculo/404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response
'''
def handler404(request, exception):
    return render(request, 'vehiculo/404.html', locals())

def handler404(request):
    return render(request, 'vehiculo/404.html', status=404)
	
def handler500(request, exception):
    return render(request, 'vehiculo/500.html', locals())

def handler500(request):
    return render(request, 'vehiculo/500.html', status=500)

# HTTP Error 400
def bad_request(request):
	response = render_to_response('vehiculo/404.html',context_instance=RequestContext(request))
	response.status_code = 404
	return response

'''
gusanare@espol.edu.ec
'''

class HomeView(TemplateView):
	template_name = 'vehiculo/index.html'

class BusquedaView(TemplateView):
	template_name = 'vehiculo/busqueda.html'

	
def carro_new(request):
	if not request.user.is_authenticated:
		return redirect('../../vehiculo/login')
		
	if request.method == "POST":
		form = CarroForm(request.POST)
		if form.is_valid():
			carro = form.save(commit=False)
			carro.usuario = request.user
			carro.save()
			return redirect('ind')
	else:
		form = CarroForm()
		
		form.usuario = User.objects.get(id=request.user.id)
		form.fields['usuario'].initial = form.usuario.username
		form.fields['provincia'].empty_label = None
		form.fields['marca'].initial = 0
	return render(request, 'vehiculo/carro_edit.html', {'form': form})
       
def carro_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('carro_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
            
        return render(request, 'vehiculo/carro_edit.html', {'form': form})

def form_busqueda(request):
	if request.method =="POST":
		marca = request.POST.get("marca")
		modelo = request.POST.get("modelo")
		anio = request.POST.get("anio")
		
		carro = Carro.objects.filter(marca__nombre=marca, modelo__nombre=modelo, anio=anio)[0]
		carro = get_object_or_404(Carro, pk=carro.id)
		inspeccion = get_object_or_404(Inspeccion, carro_id=carro.id)
		return render(request, 'vehiculo/carro_detail.html', {'carro': carro, 'inspeccion':inspeccion})

	else :
		marcas = Marca.objects.all()
		modelos = Modelo.objects.all()
			
		return render(request, 'vehiculo/carro_search.html', {'marcas': marcas, 'modelos':modelos})
			
def carro_detail(request, pk):
	carro = get_object_or_404(Carro, pk=pk)
	inspeccion = get_object_or_404(Inspeccion, carro_id=carro.id)
	
	return render(request, 'vehiculo/carro_detail.html', {'carro': carro, 'inspeccion':inspeccion})
	
	
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            persona = form.save(commit=False)

			
            
            cedula = form.cleaned_data['cedula']
            username = form.cleaned_data['username']
            correo = form.cleaned_data['email']
            password1 = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')			
            persona = Persona( cedula=cedula, username=username, correo=correo)
            persona.save()
            user = User.objects.create_user(username=username, password=password1, email=correo, first_name=first_name, last_name=last_name)            
            user.save()			
            '''
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            '''
            return redirect('ind')
    else:
        form = SignUpForm()
    return render(request, 'vehiculo/signup.html', {'form': form})	
	
	
def login_(request):

    if request.method == "POST":
    	username = request.POST['username']
    	password = request.POST['password']
    	user = auth.authenticate(username=username, password=password)
    
    	if user is not None and user.is_active:
    		auth.login(request, user)
    		return HttpResponseRedirect("../new/")
    	else:
    		return HttpResponseRedirect("invalid/")
    else:
    	return render(request, 'vehiculo/login.html')

def logout_(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/vehiculo/ind")