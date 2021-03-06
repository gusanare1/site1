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
from django.urls import include, path
from vehiculo import views

from django_private_chat import urls as django_private_chat_urls
 
handler404 = 'vehiculo.views.handler404'
handler500 = 'vehiculo.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
	path(r'', include('django_private_chat.urls')),
	path('vehiculo/', include('vehiculo.urls')),
	#path(r'', views.CarroListView.as_view()),

]
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

	