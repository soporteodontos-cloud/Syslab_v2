from dal_select2.widgets import ModelSelect2
from django import forms

from core.models import Sucursal, Especialidad, Paciente, TipoTrabajo, TipoOrdenAreas, Vendedor
from ordenes.models import OrdenTrabajo, OrdenDetalle, OrdenFoto, OrdenesTrabajoEstado, MetodoRetiro
from users.models import CustomUsers


class MetodoRetiroModelForm(forms.ModelForm):
	class Meta:
		model = MetodoRetiro
		fields = {'descripcion'}


class OrdenTrabajoNuevoModelForm(forms.ModelForm):
	class Meta:
		model = OrdenTrabajo
		fields = ['fechaSolicitud', 'clinicaExterna', 'paciente', 'vendedor', 'observacion']
		widgets = {
			'fechaSolicitud': forms.TextInput(attrs={'type': 'date'}),
			'clinicaExterna': ModelSelect2(url='clinica-autocomplete'),
			'paciente': ModelSelect2(url='paciente-autocomplete'),
			'vendedor': ModelSelect2(url='vendedorfiltrado-autocomplete'),
			'observacion': forms.Textarea()
		}

	#fechaSolicitud = forms.DateField(widget=forms.SelectDateWidget(years=range(2023, 2100)))


class OrdenTrabajoModificacionModelForm(forms.ModelForm):
	class Meta:
		model = OrdenTrabajo
		fields = ['clinicaExterna', 'paciente', 'vendedor', 'motivoModificacion']
		widgets = {
			'clinicaExterna': ModelSelect2(url='clinica-autocomplete'),
			'paciente': ModelSelect2(url='paciente-autocomplete'),
			'vendedor': ModelSelect2(url='vendedorfiltrado-autocomplete'),
			'motivoModificacion': forms.Textarea()
		}


class OrdenTrabajoEditModelForm(forms.ModelForm):
	clinicaExternaNombre = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
										   label='Clínica Externa')
	pacienteNombre = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
									 label='Paciente')
	vendedorNombre = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
									 label='Vendedor')

	class Meta:
		model = OrdenTrabajo
		fields = ['fechaSolicitud', 'clinicaExterna', 'paciente', 'vendedor', 'observacion', 'envioCourrier',
				  'metodoEnvio', 'estado', 'trabajoRepetido']
		widgets = {
			'fechaSolicitud': forms.TextInput(attrs={'readonly': 'readonly'}),
			'estado': forms.TextInput(attrs={'readonly': 'readonly'}),
			'clinicaExterna': forms.HiddenInput(),
			'paciente': forms.HiddenInput(),
			'vendedor': forms.HiddenInput(),
			'observacion': forms.Textarea(attrs={'rows': '4'}),
			'metodoEnvio': forms.Select(attrs={'onchange': 'change_metodo();'}),
		}


class OrdenDetalleModelForm(forms.ModelForm):
	class Meta:
		model = OrdenDetalle
		fields = ['orden', 'express', 'categoria', 'trabajo', 'color', 'dientes', 'maxilarSuperiorCompleto',
				  'maxilarInferiorCompleto', 'fechaEntrega', 'modoEnvio', 'observacion']
		widgets = {
			'orden': forms.HiddenInput(),
			'categoria': ModelSelect2(url='categoria-autocomplete'),
			'trabajo': ModelSelect2(url='tipotrabajofiltrado-autocomplete', forward=['categoria']),
			'color': ModelSelect2(url='colordetalle-autocomplete'),
			'dientes': forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple'}),
			'fechaEntrega': forms.TextInput(attrs={'type': 'date'}),
			'observacion': forms.Textarea(attrs={'rows': '3'})
		}


class OrdenDetalleTecnicoModelForm(forms.ModelForm):
	tecnico = forms.ModelChoiceField(queryset=CustomUsers.objects.filter(is_active=True, groups__name__in=['Tecnico']), required=True,
									 widget=ModelSelect2(url='tecnicos-autocomplete'))

	class Meta:
		model = OrdenDetalle
		fields = ['tecnico', 'observacionTecnico']
		widgets = {
			#'tecnico': ModelSelect2(url='tecnicos-autocomplete'),
			'observacionTecnico': forms.Textarea()
		}


class OrdenDetalleEntregaModelForm(forms.ModelForm):
	modoRetiro = forms.ModelChoiceField(queryset=MetodoRetiro.objects.filter(activo=True),
									 required=True,
									 widget=ModelSelect2(url='mretiro-autocomplete'), label="Modo de retiro")

	class Meta:
		model = OrdenDetalle
		fields = ['modoRetiro', 'factura', 'facturaDocumento']
		widgets = {
			#'modoRetiro': ModelSelect2('mretiro-autocomplete')
		}


class OrdenFotoModelForm(forms.ModelForm):
	class Meta:
		model = OrdenFoto
		fields = ['orden', 'foto']


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

class BuscadorOrdenes(forms.Form):
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
	desde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}), required=False,
							label="Desde")
	hasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}), required=False,
							label="Hasta")
	particulares = forms.BooleanField(required=False)
	odontos = forms.BooleanField(required=False)
	estado = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ESTADOS, required=False)
	area = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=AREAS, required=False)

class BuscadorOrdenesVendedores(forms.Form):
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
	desde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}), required=False,
							label="Desde")
	hasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}), required=False,
							label="Hasta")
	particulares = forms.BooleanField(required=False)
	odontos = forms.BooleanField(required=False)
	vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.filter(activo=True),
									  widget=ModelSelect2(url='vendedor-autocomplete'), required=False,
									  label="Vendedor")
	estado = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ESTADOS, required=False)
	area = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=AREAS, required=False)


class BuscadorOrdenesSupervisor(forms.Form):
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
	desde = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}), required=False,
							label="Desde")
	hasta = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}), required=False,
							label="Hasta")
	particulares = forms.BooleanField(required=False)
	odontos = forms.BooleanField(required=False)
	insumos = forms.BooleanField(required=False)
	estado = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ESTADOS, required=False)
	area = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=AREAS, required=False)


class OrdenesTrabajoEstadoModelForm(forms.ModelForm):
	class Meta:
		model = OrdenesTrabajoEstado
		fields = ['motivo', 'imagen']
		widgets = {
			'motivo': forms.Textarea()
		}


class OrdenesTrabajoEstadoPausarModelForm(forms.ModelForm):
	class Meta:
		model = OrdenesTrabajoEstado
		fields = ['motivo']
		widgets = {
			'motivo': forms.Textarea()
		}


class OrdenDetalleSectorModelForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		tipo_trabajo = kwargs.pop('tipo_trabajo')
		super().__init__(*args, **kwargs)
		areas = TipoOrdenAreas.objects.filter(tipoTrabajo=tipo_trabajo).values_list('area', flat=True)
		self.fields['etapaActual'] = forms.ChoiceField(choices=[(area, area) for area in areas])

	class Meta:
		model = OrdenDetalle
		fields = ['etapaActual', 'etapaOrden']
		widgets = {
			'etapaOrden': forms.HiddenInput()
		}