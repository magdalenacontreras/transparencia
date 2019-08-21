from django.contrib import admin
from .models import  NivelGobierno
from .models import  Periodo
from .models import  Ley
from .models import  Articulo
from .models import  Archivo
from .models import  Responsable


# Register your models here.

admin.site.register(NivelGobierno)
admin.site.register(Periodo)
admin.site.register(Ley)
admin.site.register(Articulo)
admin.site.register(Archivo)
admin.site.register(Responsable)

