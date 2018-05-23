'''
wordpress password
xnL!SgxGAgFPlK)4RI
'''

from django.contrib import admin

# Register your models here.

from .models import Color, Marca, Modelo, Provincia, Ciudad, Carro, Persona, Ant, Inspeccion

admin.site.register(Color)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Provincia)
admin.site.register(Ciudad)
admin.site.register(Carro)
admin.site.register(Persona)

admin.site.register(Inspeccion)

admin.site.register(Ant)
