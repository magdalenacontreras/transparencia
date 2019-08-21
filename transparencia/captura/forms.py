from django.forms import ModelForm
from captura.models import Archivo,Vinculo



class ArchivoForm(ModelForm):
	class Meta:
		model=Archivo
		fields = ['inicio_actualizacion','actualizacion' ,'validacion','anio','articulo','documento']
		labels = {
			"inicio_actualizacion": "Fecha de inicio del Periodo que se informa",
			"actualizacion": "Fecha de fin del Periodo que se informa",
		}
class VinculoForm(ModelForm):
	class Meta:
		model=Vinculo
		fields = ['nombre','descripcion','documento']
