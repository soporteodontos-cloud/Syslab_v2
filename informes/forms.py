from dal_select2.widgets import ModelSelect2
from django import forms

from core.models import Sucursal, Especialidad, Paciente, TipoTrabajo


class FiltroCargaEntrega(forms.Form):
	cargaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								 label="Carga Desde", required=False)
	cargaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								 label="Carga Hasta", required=False)
	entregaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								   label="Entrega Desde", required=False)
	entregaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								   label="Entrega Hasta", required=False)


# class FiltroCargaEntregaUsuario(forms.Form):
# 	cargaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
# 								 label="Carga Desde", required=False)
# 	cargaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
# 								 label="Carga Hasta", required=False)
# 	entregaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
# 								   label="Entrega Desde", required=False)
# 	entregaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
# 								   label="Entrega Hasta", required=False)

ENVIO1 = (
	('', 'Ninguno'),
	('Modificación', 'Modificación'),
	('Repetición', 'Repetición'),
)

ESTADOS = (
	('', 'Todos'),
	('COURIER ENTRANTE', 'COURIER ENTRANTE'),
	('ENTREGADO A LABORATORIO', 'ENTREGADO A LABORATORIO'),
	('INSUMO BANDEJA ENTRADA', 'INSUMO BANDEJA ENTRADA'),
	('NO CONFIRMADO', 'NO CONFIRMADO'),
	('PENDIENTE DE RETIRO/ENTREGA', 'PENDIENTE DE RETIRO/ENTREGA'),
	('PREPARADOR BANDEJA ENTRADA', 'PREPARADOR BANDEJA ENTRADA'),
	('RECHAZADO', 'RECHAZADO'),
	('TRABAJO ENTREGADO', 'TRABAJO ENTREGADO'),
	('TRABAJO INICIADO', 'TRABAJO INICIADO'),
	('TRABAJO FINALIZADO', 'TRABAJO FINALIZADO'),
)

AREAS = (
	('', 'Todas'),
	('ACRILICO', 'ACRILICO'),
	('CAD CAM', 'CAD CAM'),
	('CARGA INICIAL', 'CARGA INICIAL'),
	('INSUMOS', 'INSUMOS'),
	('LOGISTICA ENTRADA', 'LOGISTICA ENTRADA'),
	('LOGISTICA SALIDA', 'LOGISTICA SALIDA'),
	('MAQUILLAJE', 'MAQUILLAJE'),
	('METAL', 'METAL'),
	('METALOCERAMICA', 'METALOCERAMICA'),
	('TECNICOS', 'TECNICOS'),
	('YESO', 'YESO'),
)



class BuscadorOrdenesGeneralReporte(forms.Form):
	clinicaExterna = forms.ModelChoiceField(queryset=Sucursal.objects.filter(activo=True),
											widget=ModelSelect2(url='clinica-autocomplete'), required=False,
											label="Clínica Particular")
	especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.filter(activo=True),
										  widget=ModelSelect2(url='especialidad-autocomplete'), required=False,
										  label="Especialidad")  # para filtrar tipo trabajo
	orden = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False,
							   label="Nro. Trabajo")
	paciente = forms.ModelChoiceField(queryset=Paciente.objects.filter(activo=True),
									  widget=ModelSelect2(url='paciente-autocomplete'), required=False,
									  label="Paciente")
	tipoTrabajo = forms.ModelChoiceField(queryset=TipoTrabajo.objects.filter(activo=True),
										 widget=ModelSelect2(url='tipotrabajo-autocomplete'), required=False,
										 label="Tipo de Trabajo")
	cargaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								 label="Carga Desde", required=False)
	cargaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								 label="Carga Hasta", required=False)
	entregaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								   label="Entrega Desde", required=False)
	entregaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								   label="Entrega Hasta", required=False)
	estado = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ESTADOS, required=False)
	area = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=AREAS, required=False)
	metodo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ENVIO1, required=False)

class BuscadorOrdenesReporte(forms.Form):
	clinicaExterna = forms.ModelChoiceField(queryset=Sucursal.objects.filter(activo=True),
											widget=ModelSelect2(url='clinica-autocomplete'), required=False,
											label="Clínica Particular")
	especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.filter(activo=True),
										  widget=ModelSelect2(url='especialidad-autocomplete'), required=False,
										  label="Especialidad")  # para filtrar tipo trabajo
	orden = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False,
							   label="Nro. Trabajo")
	paciente = forms.ModelChoiceField(queryset=Paciente.objects.filter(activo=True),
									  widget=ModelSelect2(url='paciente-autocomplete'), required=False,
									  label="Paciente")
	tipoTrabajo = forms.ModelChoiceField(queryset=TipoTrabajo.objects.filter(activo=True),
										 widget=ModelSelect2(url='tipotrabajo-autocomplete'), required=False,
										 label="Tipo de Trabajo")
	cargaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								 label="Carga Desde", required=False)
	cargaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								 label="Carga Hasta", required=False)
	entregaDesde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								   label="Entrega Desde", required=False)
	entregaHasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
								   label="Entrega Hasta", required=False)
	metodo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ENVIO1, required=False)