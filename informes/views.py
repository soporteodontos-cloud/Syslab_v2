from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your views here.
from informes.forms import FiltroCargaEntrega, BuscadorOrdenesReporte, BuscadorOrdenesGeneralReporte


def trabajoPorArea(request):

	ini = {'cargaDesde': datetime.today().replace(day=1).date(),
		   'cargaHasta': (datetime.today() + relativedelta(day=31)).date()}
	print(ini)
	form = FiltroCargaEntrega(initial=ini)
	data_context = {'request': request, 'form': form}
	return render(request, 'informes/area.html', data_context)


def OrdenTrabajoReportLView(request):
	ini = {'cargaDesde': datetime.today().replace(day=1).date(),
		   'cargaHasta': (datetime.today() + relativedelta(day=31)).date()}
	print(ini)
	form = BuscadorOrdenesGeneralReporte(initial=ini)
	data_context = {'request': request, 'form': form}
	return render(request, 'informes/general.html', data_context)

def OrdenTrabajoEnProduccionReportLView(request):
	ini = {'cargaDesde': datetime.today().replace(day=1).date(),
		   'cargaHasta': (datetime.today() + relativedelta(day=31)).date()}
	print(ini)
	form = BuscadorOrdenesReporte(initial=ini)
	data_context = {'request': request, 'form': form}
	return render(request, 'informes/produccion.html', data_context)


def OrdenTrabajoEn24y48ReportLView(request):
	ini = {'cargaDesde': datetime.today().replace(day=1).date(),
		   'cargaHasta': (datetime.today() + relativedelta(day=31)).date()}
	print(ini)
	form = BuscadorOrdenesReporte(initial=ini)
	data_context = {'request': request, 'form': form}
	return render(request, 'informes/2448.html', data_context)


def OrdenTrabajoEntregarReportLView(request):
	ini = {'cargaDesde': datetime.today().replace(day=1).date(),
		   'cargaHasta': (datetime.today() + relativedelta(day=31)).date()}
	print(ini)
	form = BuscadorOrdenesReporte(initial=ini)
	data_context = {'request': request, 'form': form}
	return render(request, 'informes/entregar.html', data_context)