from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from users.models import CustomUsers, MY_AREAS


class Categoria(models.Model):
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='categoria_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='categoria_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class Tarea(models.Model):
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='tarea_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='tarea_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class Especialidad(models.Model):
	descripcion = models.CharField(max_length=200)
	categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='especialidad_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='especialidad_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class FaseEspecialidad(models.Model):
	especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
	descripcion = models.CharField(max_length=200, verbose_name='')
	rol = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='')
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='fase_creado_por')
	creado_el = models.DateTimeField(null=True, blank=True)


class FaseTarea(models.Model):
	fase = models.ForeignKey(FaseEspecialidad, on_delete=models.PROTECT)
	tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT, verbose_name='')
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='ftarea_creado_por')
	creado_el = models.DateTimeField(null=True, blank=True)


METODOLOGIA = (
	('DIENTES','DIENTES'),
	('MAXILAR','MAXILAR'),
	('MIXTO','MIXTO'),
)

class TipoTrabajo(models.Model):
	descripcion = models.CharField(max_length=200)
	especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
	metodologiaTrabajo = models.CharField(max_length=30, choices=METODOLOGIA, verbose_name="Metodologia de Trabajo")
	precio = models.IntegerField()
	duracionEstimadaOdontos = models.IntegerField(verbose_name="Duracion estiamada Odontos hasta 4 dientes")
	duracionEstimadaParticulares = models.IntegerField(verbose_name="Duracion estimada particulares hasta 4 dientes")
	duracionEstimadaOdontos5 = models.IntegerField(verbose_name="Duracion estiamada Odontos 5 o mas dientes")
	duracionEstimadaParticulares5 = models.IntegerField(verbose_name="Duracion estimada particulares 5 o mas dientes")
	minimoDientes = models.IntegerField(verbose_name="Minimo de Dientes")
	maximoDientes = models.IntegerField(verbose_name="Maximo de Dientes")
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='ttrabajo_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='ttrabajo_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion

	@property
	def areas(self):
		return list(self.tipoordenareas_set.order_by('orden').values_list('area', flat=True))

class TipoOrdenAreas(models.Model):
	tipoTrabajo = models.ForeignKey(TipoTrabajo, on_delete=models.CASCADE)
	orden = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name='')
	area = models.CharField(max_length=100, choices=MY_AREAS, verbose_name='')

	class Meta:
		unique_together = ('tipoTrabajo', 'orden')

TIPOCONSUMO = (
	('UNITARIO','UNITARIO'),
	('PROMEDIADO','PROMEDIADO'),
)

class Insumo(models.Model):
	descripcion = models.CharField(max_length=200)
	tipo = models.CharField(max_length=30, choices=TIPOCONSUMO, verbose_name="Tipo de Insumo")
	#cantidad = models.DecimalField(decimal_places=2, max_digits=17, verbose_name="Cantidad uso promedio")
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='insumo_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='insumo_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class TrabajoInsumo(models.Model):
	trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT)
	insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, verbose_name="")
	cantidad = models.DecimalField(max_digits=17, decimal_places=2, verbose_name="")


class Material(models.Model):
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='material_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='material_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class MarcaColor(models.Model):
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='mcolor_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='mcolor_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class ColorDetalle(models.Model):
	marca = models.ForeignKey(MarcaColor, on_delete=models.PROTECT)
	codigo = models.CharField(max_length=200, verbose_name='')
	descripcion = models.CharField(max_length=200, verbose_name='')
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='color_creado_por')
	creado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.marca.descripcion + ' - ' + self.codigo


class Vendedor(models.Model):
	nombreApellido = models.CharField(max_length=200, verbose_name="Nombre y Apellido")
	telefono = models.CharField(max_length=100, null=True, blank=True)
	ruc = models.IntegerField(null=True, blank=True)
	dv = models.IntegerField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='vendedor_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='vendedor_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.nombreApellido


class Ciudad(models.Model):
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='ciudad_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='ciudad_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


TIPOSUCURSAL = (
	('Clinica externa', 'Clinica externa'),
	('Odontos', 'Odontos')
)

class Sucursal(models.Model):
	tipo = models.CharField(max_length=30, choices=TIPOSUCURSAL, verbose_name="Tipo de Sucursal")
	descripcion = models.CharField(max_length=200, verbose_name="Nombre de Dr.")
	nombreClinica = models.CharField(max_length=200, default="Sin nombre", verbose_name="Nombre de clinica")
	razonSocial = models.CharField(max_length=200, null=True, blank=True, verbose_name="Razon social")
	ruc = models.IntegerField(null=True, blank=True)
	dv = models.IntegerField(null=True, blank=True)
	telefono = models.CharField(max_length=100, null=True, blank=True)
	direccion = models.CharField(max_length=200, null=True, blank=True)
	ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT, null=True, blank=True)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='sucursal_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='sucursal_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.descripcion


class Paciente(models.Model):
	nombreApellido = models.CharField(max_length=200, verbose_name="Nombre y Apellido")
	razonSocial = models.CharField(max_length=200, null=True, blank=True, verbose_name="Razon social")
	ruc = models.IntegerField(null=True, blank=True)
	dv = models.IntegerField(null=True, blank=True)
	telefono = models.CharField(max_length=100, null=True, blank=True)
	direccion = models.CharField(max_length=200, null=True, blank=True)
	ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	activo = models.BooleanField(default=True)
	creado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
								   blank=True, related_name='paciente_creado_por')
	modificado_por = models.ForeignKey(CustomUsers, on_delete=models.PROTECT, null=True,
									   blank=True, related_name='paciente_modificado_por')
	creado_el = models.DateTimeField(null=True, blank=True)
	modificado_el = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.nombreApellido







