from django.urls import path, include

from ordenes.api import get_met_trabajo, save_orden_trabajo, get_orden_trabajo, change_orden_trabajo
from ordenes.views import OrdenTrabajoCreateView, OrdenTrabajoUpdateView, OrdenTrabajoListView, \
	OrdenTrabajoHistorialListView, OrdenTrabajoDeleteView, vaciadoAccion, pasarInsumosAccion, rechazarInsumosAccion, \
	InsumosOrdenListView, pasarTecnicosAccion, iniciarAccion, asignarTecnicoAccion, finalizarAccion, \
	enviarLogisticaAccion, entregaAccion, MetodoRetiroaListView, MetodoRetiroCreateView, MetodoRetiroUpdateView, \
	MetodoRetiroDeleteView, pausarInsumosAccion, continuarInsumosAccion, rechazarProduccionAccion, entregaRechazoAccion, \
	OrdenTrabajoUpdate1View, etapasAccion, enviarAccion, OrdenDetalleSectorUpdateView, recepcionarTrabajo

urlpatterns = [

	path(r'mretiro/list', MetodoRetiroaListView, name='mretiro_list'),
	path(r'mretiro/create', MetodoRetiroCreateView.as_view(), name='mretiro_create'),
	path(r'mretiro/update/<int:pk>/', MetodoRetiroUpdateView.as_view(), name='mretiro_update'),
	path(r'mretiro/delete/<int:pk>/', MetodoRetiroDeleteView.as_view(), name='mretiro_delete'),

	path(r'', OrdenTrabajoListView, name='orden_list'),
	path(r'history/<int:pk>/', OrdenTrabajoHistorialListView, name='orden_historial_list'),
	path(r'create', OrdenTrabajoCreateView.as_view(), name='orden_create'),
	path(r'update/<int:pk>/', OrdenTrabajoUpdateView, name='orden_update'),
	path(r'delete/<int:pk>/', OrdenTrabajoDeleteView.as_view(), name='orden_delete'),
	path(r'update1/<int:pk>/', OrdenTrabajoUpdate1View.as_view(), name='orden_update1'),

	path(r'workmet/<int:pk>/', get_met_trabajo, name='get_met_trabajo'),
	path(r'workorder/', save_orden_trabajo, name='save_orden_trabajo'),
	path(r'workorder/<int:pk>/', get_orden_trabajo, name='get_orden_trabajo'),
	path(r'workorder/delete/', change_orden_trabajo, name='change_orden_trabajo'),
	path(r'workorder/vaciado/<int:pk>/', vaciadoAccion, name='vaciadoAccion'),
	path(r'workorder/recepcionar/<int:pk>/', recepcionarTrabajo, name='recepcionarTrabajo'),
	path(r'workorder/pinsumos/<int:pk>/', pasarInsumosAccion, name='pasarInsumosAccion'),
	path(r'workorder/rinsumos/<int:pk>/', rechazarInsumosAccion, name='rechazarInsumosAccion'),
	path(r'workorder/insumos/<int:pk>/', InsumosOrdenListView, name='InsumosOrdenListView'),
	path(r'workorder/ptecnicos/<int:pk>/', pasarTecnicosAccion, name='pasarTecnicosAccion'),
	path(r'workorder/iniciar/<int:pk>/<str:area>/<str:orden>/<int:user>/', iniciarAccion, name='iniciarAccion'),
	path(r'workorder/enviar/<int:pk>/<str:area>/<str:orden>/', enviarAccion, name='enviarAccion'),
	path(r'workorder/asignart/<int:pk>/', asignarTecnicoAccion, name='asignarTecnicoAccion'),
	path(r'workorder/finalizar/<int:pk>/<str:area>/<str:orden>/', finalizarAccion, name='finalizarAccion'),
	path(r'workorder/elogistica/<int:pk>/', enviarLogisticaAccion, name='enviarLogisticaAccion'),
	path(r'workorder/entrega/<int:pk>/', entregaAccion, name='entregaAccion'),
	path(r'workorder/entregar/<int:pk>/', entregaRechazoAccion, name='entregaRechazoAccion'),
	path(r'workorder/ipausar/<int:pk>/', pausarInsumosAccion, name='pausarInsumosAccion'),
	path(r'workorder/ireanudar/<int:pk>/', continuarInsumosAccion, name='continuarInsumosAccion'),
	path(r'workorder/rproduccion/<int:pk>/', rechazarProduccionAccion, name='rechazarProduccionAccion'),
	path(r'workorder/etapa/<int:pk>/<int:etapa>/', etapasAccion, name='etapasAccion'),
	path(r'workorder/sector/<int:pk>/', OrdenDetalleSectorUpdateView.as_view(), name='OrdenDetalleSectorUpdateView'),
]
