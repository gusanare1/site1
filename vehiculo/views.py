from django.shortcuts import render,redirect,get_object_or_404
from .forms import CarroForm, SignUpForm, BusquedaForm
from .models import Color, Marca, Modelo, Provincia, Ciudad, Carro, Inspeccion, Persona
# Create your views here.
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib import auth
from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage

from django.contrib import messages
from PIL import Image
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


def mensaje(request, mensaje):
    messages.success(request, mensaje)


class CarroListView(ListView):
	template_name = 'vehiculo/index.html'
	model = Carro
	queryset = Carro.objects.filter(esta_inspeccionado=True)
	context_object_name='carro_list'
	paginate_by = 4

class BusquedaView(TemplateView):
	template_name = 'vehiculo/busqueda.html'



def carro_new(request):

	if not request.user.is_authenticated:
		#request.session['error'] = "No logueado"
		request.session['ver']= True
		mensaje(request, 'No logueado')
		return redirect('../../vehiculo/login')
	#Guardando la imagen resizeado
	size = (480,320)

	if request.method == "POST":
		form = CarroForm(request.POST)
		if form.is_valid():
			import re
			carro = form.save(commit=False)
			carro.usuario = request.user
			#No usamos form-clean porque lo estoy trayendo de post...
			modelo = request.POST.get('modelo')
			modelo_ = modelo.replace(' ','') #	quitamos los espacios (no son alfanumericos)
			patron ="\W" #CARACTERES NO ALFANUMERICOS (posible danino)
			if re.search(patron, modelo_):
				carro.save() #lanza error....
			else:
				carro.modelo = Modelo.objects.get(id=modelo)

			myfile = request.FILES['imagen']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			carro.imagen_nombre = fs.url(filename)

			import os
			if os.name == 'posix':
				#name = 'media/'+filename
				name_ = os.path.join(os.path.dirname(os.path.dirname(__file__)),'media/',filename)
			else:
				#name = 'C:\\Users\\lenov\\Documents\\python_Win_Deb\\site1\\media\\'+filename
				name_ = 'C:\\Users\\lenov\\Documents\\python_Win_Deb\\site1\\media\\'+filename

			n,e = os.path.splitext(name_)
			name = n+"thumbnail"+e
			img = Image.open(name_)
			img.resize(size).save(name)

			from apiclient.discovery import build
			from httplib2 import Http
			from oauth2client import file, client, tools
			from apiclient.http import MediaFileUpload

			# Setup the Drive v3 API
			SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file'
			store = file.Storage('credentials.json')
			creds = store.get()
			if not creds or creds.invalid:
				flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
				creds = tools.run_flow(flow, store)
			service = build('drive', 'v3', http=creds.authorize(Http()))

			folder_id = '158Sk_z9ERQR5pSY94x1bhw4_SOGeUjgg'
			file_metadata = {
				'name': filename,
				'parents': [folder_id]
			}
			media = MediaFileUpload(name,
									mimetype='image/jpeg',
									resumable=True)
			file = service.files().create(body=file_metadata,
												media_body=media,
												fields='id').execute()





			#print('File ID: %s' % file.get('id'))
			carro.imagen_nombre = file.get('id')

			ciudad = request.POST.get('ciudad')
			ciudad_ = ciudad.replace(' ','') #	quitamos los espacios (no son alfanumericos)
			patron ="\W" #CARACTERES NO ALFANUMERICOS (posible danino)
			if re.search(patron, ciudad_):
				carro.save() #lanza error....
			else:
				carro.ciudad = Ciudad.objects.get(id=ciudad)
			carro.save()

			request.session['ver']=True
			mensaje(request, "Carro "+carro.placa+" creado")
			'''
			import os
			os.remove(name)
			'''
			return redirect('ind')
	else:
	    form = CarroForm()
	    form.usuario = User.objects.get(id=request.user.id)
	    form.fields['usuario'].initial = form.usuario.username
		#form.fields['provincia'].empty_label = None
		#form.fields['marca'].initial = 0
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

		carros = Carro.objects.filter(marca__nombre=marca, modelo__nombre=modelo, anio=anio)[0]
		carro = get_object_or_404(Carro, pk=carro.id)
		inspeccion = get_object_or_404(Inspeccion, carro_id=carro.id)
		return render(request, 'vehiculo/carro_detail.html', {'carro': carro, 'inspeccion':inspeccion})

	else :
		marcas = Marca.objects.all()
		modelos = Modelo.objects.all()

		return render(request, 'vehiculo/carro_search.html', {'marcas': marcas, 'modelos':modelos})

'''
SI NO HAY INSPECCION, NO SE MEUESTRA EL CARRO
'''
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
            mensaje(request, "Usuario creado")
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