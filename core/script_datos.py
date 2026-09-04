from django.contrib.auth.models import Group
from django.utils import timezone

from core.models import Categoria, Especialidad, TipoTrabajo

grupos = [
	'Administrador',
	'Asistente de Profesional',
	'Carga de insumos',
	'Consultor',
	'Consultora',
	'Delivery',
	'Encargado de Compras',
	'Encargado de sistema',
	'Logistica',
	'Paciente',
	'Tecnico',
	'Preparador',
	'Supervisor de Asistente Profesional',
	'Supervisor Tecnico'
]

categorias = [
	{
		'nombre': 'CAD CAM',
		'especialidad': [
			{'nombre': 'CAD CAM + MAQUILLAJE',
			 'tipotrabajo': [
				 'CARILLA DE DISILICATO DE LITIO',
				 'CARILLA DE PORCELANA PURA POR PIEZA',
				 'CARILLA DE ZIRCONIO'
			 ]
			 }
		]
	},
]


def iniciales():
	for g in grupos:
		grupo, created = Group.objects.get_or_create(name=g)

	for c in categorias:
		categoria, created = Categoria.objects.get_or_create(descripcion=c['nombre'], creado_por_id=1,
															 creado_el=timezone.now())
		for e in c['especialidad']:
			especialida, created = Especialidad.objects.get_or_create(categoria=categoria, descripcion=e['nombre'],
																	  creado_por_id=1, creado_el=timezone.now())
			for t in e['tipotrabajo']:
				tipotrabajo, created = TipoTrabajo.objects.get_or_create(especialidad=especialida,
																		 descripcion=t,
																		 precio=0,
																		 duracionEstimadaOdontos=1,
																		 duracionEstimadaParticulares=1,
																		 minimoDientes=1,
																		 maximoDientes=1,
																		 creado_por_id=1,
																		 creado_el=timezone.now(),
																		 duracionEstimadaOdontos5=1,
																		 duracionEstimadaParticulares5=1)
