from django.urls import path, include

from informes.api import getTrabajosPorArea
from informes.views import trabajoPorArea, OrdenTrabajoReportLView, OrdenTrabajoEnProduccionReportLView, \
	OrdenTrabajoEn24y48ReportLView, OrdenTrabajoEntregarReportLView

urlpatterns = [
	path(r'trabajoarea', trabajoPorArea, name='trabajoPorArea'),
	path(r'general', OrdenTrabajoReportLView, name='OrdenTrabajoReportLView'),
	path(r'produccion', OrdenTrabajoEnProduccionReportLView, name='OrdenTrabajoEnProduccionReportLView'),
	path(r'vencer', OrdenTrabajoEn24y48ReportLView, name='OrdenTrabajoEn24y48ReportLView'),
	path(r'entregar', OrdenTrabajoEntregarReportLView, name='OrdenTrabajoEntregarReportLView'),

]