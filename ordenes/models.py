from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords

from core.models import Sucursal, Paciente, Vendedor, Categoria, TipoTrabajo, ColorDetalle
from users.models import CustomUsers

DIENTES = (
	('11', '11'),
	('12', '12'),
	('13', '13'),
	('14', '14'),
	('15', '15'),
	('16', '16'),
	('17', '17'),
	('18', '18'),

	('21', '21'),
	('22', '22'),
	('23', '23'),
	('24', '24'),
	('25', '25'),
	('26', '26'),
	('27', '27'),
	('28', '28'),

	('31', '31'),
	('32', '32'),
	('33', '33'),
	('34', '34'),
	('35', '35'),
	('36', '36'),
	('37', '37'),
	('38', '38'),

	('41', '41'),
	('42', '42'),
	('43', '43'),
	('44', '44'),
	('45', '45'),
	('46', '46'),
	('47', '47'),
	('48', '48')
)

ENVIO = (
	('Modelo', 'Modelo'),
	('Escaneado', 'Escaneado'),
	('Impreso', 'Impreso'),
)

ENVIO1 = (
	('Ninguno', 'Ninguno'),
	('Modificación', 'Modificación'),
	('Repetición', 'Repetición'),
)

class MetodoRetiro(models.Model):
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='metodoRetiro_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='metodoRetiro_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion

from django.core.exceptions import ValidationError

class OrdenTrabajo(models.Model):
	fechaSolicitud = models.DateField(verbose_name="Fecha Solicitud")
	clinicaExterna = models.ForeignKey(Sucursal, on_delete=models.PROTECT, verbose_name="Clínica Externa")
	paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
	vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT)
	observacion = models.CharField(max_length=5000, null=True, blank=True)
	estado = models.CharField(max_length=500, null=True, blank=True, default="COURIER ENTRANTE")
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='orden_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='orden_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	envioCourrier = models.BooleanField(default=False, verbose_name="Envio Courrier")
	metodoEnvio = models.CharField(max_length=50, choices=ENVIO1, default="Ninguno", verbose_name="Método de reenvío de trabajo")
	trabajoRepetido = models.IntegerField(null=True, blank=True, verbose_name="Nº trabajo a repetir")
	motivoModificacion = models.CharField(max_length=5000, null=True, blank=True, verbose_name="Motivo")
	history = HistoricalRecords()

	def __str__(self):
		return self.paciente.nombreApellido + ' / ' + self.fechaSolicitud.strftime('%d-%m-%Y')

	def clean(self):
		if self.fechaSolicitud.year < 2023:
			raise ValidationError('La fecha de solicitud no puede ser menor al año 2023.')

MODORETIRO = (
	('DELIVERY', 'DELIVERY'),
	('RETIRO EN SALON', 'RETIRO EN SALON')
)

class OrdenDetalle(models.Model):
	orden = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT)
	express = models.BooleanField(default=False, verbose_name="Trabajo Express")
	categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
	trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT, null=True, blank=True)
	color = models.ForeignKey(ColorDetalle, on_delete=models.PROTECT, null=True, blank=True)
	dientes = MultiSelectField(choices=DIENTES, max_length=5000, null=True, blank=True)
	maxilarSuperiorCompleto = models.BooleanField(default=False, verbose_name="Maxilar Superior Completo")
	maxilarInferiorCompleto = models.BooleanField(default=False, verbose_name="Maxilar Inferior Completo")
	fechaEntrega = models.DateField(verbose_name="Fecha de Entrega", null=True, blank=True)
	modoEnvio = models.CharField(max_length=50, choices=ENVIO, default="Modelo", verbose_name="Se envía")
	observacion = models.CharField(max_length=5000, blank=True, null=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='ordentrabajo_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='ordentrabajo_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)
	activo = models.BooleanField(default=True)
	estado = models.CharField(max_length=500, null=True, blank=True)
	area = models.CharField(max_length=500, null=True, blank=True)
	tecnico = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True, blank=True)
	observacionTecnico = models.CharField(max_length=5000, blank=True, null=True, verbose_name="Observacion")
	#modoRetiro = models.CharField(max_length=50, choices=MODORETIRO, null=True, blank=True)
	modoRetiro = models.ForeignKey(MetodoRetiro, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Modo de retiro")
	factura = models.CharField(max_length=30, null=True, blank=True)
	facturaDocumento = models.FileField(upload_to='facturas/', verbose_name='Fichero', null=True, blank=True)
	etapaActual = models.CharField(max_length=100, null=True, blank=True, verbose_name="Etapa actual")
	etapaOrden = models.IntegerField(null=True, blank=True)


class OrdenFoto(models.Model):
	orden = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT)
	foto = models.ImageField(upload_to='orden/', verbose_name='')


class OrdenesTrabajoEstado(models.Model):
	fechaHora = models.DateTimeField(auto_now_add=True)
	orden = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT)
	trabajo = models.ForeignKey(OrdenDetalle, on_delete=models.DO_NOTHING, null=True, blank=True)
	estado = models.CharField(max_length=500, null=True, blank=True)
	area = models.CharField(max_length=500, null=True, blank=True)
	usuario = models.ForeignKey(CustomUsers, null=True, blank=True, on_delete=models.DO_NOTHING)
	motivo = models.CharField(max_length=5000, null=True, blank=True)
	imagen = models.ImageField(upload_to='rechazos/', verbose_name='', null=True, blank=True)

