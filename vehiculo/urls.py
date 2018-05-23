"""site1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from .ajax import get_ciudades, get_modelos, get_cars_by_model_name, get_model_name

urlpatterns = [

		path(r'busqueda/', views.form_busqueda, name='busqueda'),
        path(r'ind/', views.CarroListView.as_view(), name='ind'),
        path(r'busqueda/<int:pk>/', views.carro_detail, name="carro_detail"),
        path(r'new/', views.carro_new, name='carro_new'),
		path(r'ajax/get_ciudades', get_ciudades, name = 'get_ciudades'),
		path(r'ajax/get_modelos', get_modelos, name = 'get_modelos'),
    path(r'ajax/get_cars_by_model_name', get_cars_by_model_name, name = 'get_cars_by_model_name'),
path(r'ajax/get_model_name', get_model_name, name = 'get_model_name'),
	
	path(r'login/',  views.login_, name='login_'),
    path(r'logout/', views.logout_, name='logout_'),
	path(r'signup/', views.signup, name='signup_'),
	]