from django.contrib.auth.decorators import permission_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView

from core.models import TipoOrdenAreas
from ordenes.forms import OrdenTrabajoNuevoModelForm, OrdenTrabajoEditModelForm, OrdenDetalleModelForm, \
	OrdenFotoModelForm, BuscadorOrdenes, OrdenesTrabajoEstadoModelForm, OrdenDetalleTecnicoModelForm, \
	OrdenDetalleEntregaModelForm, MetodoRetiroModelForm, OrdenesTrabajoEstadoPausarModelForm, \
	OrdenTrabajoModificacionModelForm, OrdenDetalleSectorModelForm, BuscadorOrdenesSupervisor, \
	BuscadorOrdenesVendedores
from ordenes.models import OrdenTrabajo, OrdenesTrabajoEstado, OrdenDetalle, OrdenFoto, MetodoRetiro


@permission_required('ordenes.view_metodoretiro', raise_exception=True)
def MetodoRetiroaListView(request):
	data_context = {'request': request}
	return render(request, 'mretiro/list.html', data_context)


class MetodoRetiroCreateView(CreateView):
	model = MetodoRetiro
	form_class = MetodoRetiroModelForm
	success_url = reverse_lazy('mretiro_list')
	template_name = 'mretiro/form.html'

	@method_decorator(permission_required('ordenes.add_metodoretiro', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MetodoRetiroCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MetodoRetiroCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class MetodoRetiroUpdateView(UpdateView):
	model = MetodoRetiro
	form_class = MetodoRetiroModelForm
	success_url = reverse_lazy('mretiro_list')
	template_name = 'mretiro/form.html'

	@method_decorator(permission_required('ordenes.change_metodoretiro', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MetodoRetiroUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MetodoRetiroUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class MetodoRetiroDeleteView(DeleteView):
	model = MetodoRetiro
	template_name = 'mretiro/delete.html'
	success_url = reverse_lazy('mretiro_list')

	@method_decorator(permission_required('ordenes.delete_metodoretiro', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MetodoRetiroDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


class OrdenTrabajoCreateView(CreateView):
	model = OrdenTrabajo
	form_class = OrdenTrabajoNuevoModelForm
	success_url = reverse_lazy('paciente_list')
	template_name = 'ordenes/form1.html'

	@method_decorator(permission_required('ordenes.add_ordentrabajo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(OrdenTrabajoCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(OrdenTrabajoCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		if form.cleaned_data['fechaSolicitud'].year < 2023:
			form.add_error('fechaSolicitud', 'La fecha de solicitud no puede ser menor al año 2023.')
			return super().form_invalid(form)
		else:
			self.object = form.save(commit=False)
			self.object.creado_por = self.request.user
			self.object.creado_el = timezone.now()
			self.object.estado = "PEDIDO NO CONFIRMADO"
			self.object.save()
			trabajo = OrdenDetalle()
			trabajo.orden = self.object
			trabajo.estado = "COURIER ENTRANTE"
			trabajo.area = "LOGISTICA ENTRADA"
			trabajo.save()
			return HttpResponseRedirect('/ordenes/update/' + str(self.object.pk) + '/')


class OrdenTrabajoUpdate1View(UpdateView):
	model = OrdenTrabajo
	form_class = OrdenTrabajoModificacionModelForm
	success_url = reverse_lazy('paciente_list')
	template_name = 'ordenes/form1.html'

	@method_decorator(permission_required('ordenes.change_ordentrabajo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(OrdenTrabajoUpdate1View, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(OrdenTrabajoUpdate1View, self).get_context_data(**kwargs)

		especialidad = self.request.GET.get('especialidad', None)
		clinica = self.request.GET.get('clinica', None)
		tipoTrabajo = self.request.GET.get('tipoTrabajo', None)
		paciente = self.request.GET.get('paciente', None)
		desde = self.request.GET.get('desde', None)
		hasta = self.request.GET.get('hasta', None)
		particulares = self.request.GET.get('particulares', None)
		odontos = self.request.GET.get('odontos', None)
		area = self.request.GET.get('area', None)
		estado = self.request.GET.get('estado', None)

		if especialidad == "null":
			especialidad = ''
		if clinica == "null":
			clinica = ''
		if tipoTrabajo == "null":
			tipoTrabajo = ''
		if paciente == "null":
			paciente = ''
		if desde == "null":
			desde = ''
		if hasta == "null":
			hasta = ''
		if area == "null":
			area = ''
		if estado == "null":
			estado = ''
		if particulares == "True" or particulares == "true":
			particulares = True
		else:
			particulares = False
		if odontos == "True" or odontos == "true":
			odontos = True
		else:
			odontos = False

		context['request'] = self.request
		context['especialidad'] = especialidad
		context['clinica'] = clinica
		context['tipoTrabajo'] = tipoTrabajo
		context['paciente'] = paciente
		context['desde'] = desde
		context['hasta'] = hasta
		context['particulares'] = particulares
		context['odontos'] = odontos
		context['area'] = area
		context['estado'] = estado
		return context

	def form_valid(self, form):

		especialidad = self.request.GET.get('especialidad', None)
		clinica = self.request.GET.get('clinica', None)
		tipoTrabajo = self.request.GET.get('tipoTrabajo', None)
		paciente = self.request.GET.get('paciente', None)
		desde = self.request.GET.get('desde', None)
		hasta = self.request.GET.get('hasta', None)
		particulares = self.request.GET.get('particulares', None)
		odontos = self.request.GET.get('odontos', None)
		area = self.request.GET.get('area', None)
		estado = self.request.GET.get('estado', None)

		if especialidad == "null":
			especialidad = ''
		if clinica == "null":
			clinica = ''
		if tipoTrabajo == "null":
			tipoTrabajo = ''
		if paciente == "null":
			paciente = ''
		if desde == "null":
			desde = ''
		if hasta == "null":
			hasta = ''
		if area == "null":
			area = ''
		if estado == "null":
			estado = ''
		if particulares == "True" or particulares == "true":
			particulares = True
		else:
			particulares = False
		if odontos == "True" or odontos == "true":
			odontos = True
		else:
			odontos = False

		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area)+'&estado='+str(estado))


@permission_required('ordenes.change_ordentrabajo', raise_exception=True)
def OrdenTrabajoUpdateView(request, pk):

	especialidad = request.GET.get('especialidad', 'null')
	clinica = request.GET.get('clinica', 'null')
	tipoTrabajo = request.GET.get('tipoTrabajo', 'null')
	paciente = request.GET.get('paciente', 'null')
	desde = request.GET.get('desde', 'null')
	hasta = request.GET.get('hasta', 'null')
	particulares = request.GET.get('particulares', 'false')
	odontos = request.GET.get('odontos', 'false')
	area = request.GET.get('area', 'null')
	estado = request.GET.get('estado', 'null')


	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
	permisos = list(l)
	form = BuscadorOrdenes()
	if len(permisos) > 0:
		permisos = permisos[0]
	else:
		permisos = ''
	main = OrdenTrabajo.objects.get(pk=pk)
	main.modificado_por = request.user
	main.modificado_el = timezone.now()
	fotos = inlineformset_factory(OrdenTrabajo, OrdenFoto, form=OrdenFotoModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		trabajo = OrdenDetalleModelForm()
		form = OrdenTrabajoEditModelForm(request.POST, instance=main)
		formset = fotos(request.POST, request.FILES, instance=main, prefix="fotos")
		print(form.errors)
		print(formset.errors)
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			if permisos == "Logistica":
				main.estado = "PEDIDO CONFIRMADO"
				main.save()
				trabajos = OrdenDetalle.objects.filter(orden=main)
				for t in trabajos:
					t.estado = "PREPARADOR BANDEJA ENTRADA"
					t.area = "YESO"
					t.save()
					e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main, trabajo=t,
																			 estado="Se confirma el trabajo.",
																			 area="CARGA INICIAL",
																			 usuario=request.user)
					e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main, trabajo=t,
																				 estado="La orden pasa a insumos.",
																				 area="YESO",
																				 usuario=request.user)
				e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main,
																			 estado="PEDIDO CONFIRMADO")
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area)+'&estado='+str(estado))
	else:
		form = OrdenTrabajoEditModelForm(instance=main, initial={'clinicaExternaNombre': main.clinicaExterna.descripcion,
																 'pacienteNombre': main.paciente.nombreApellido,
										 						 'vendedorNombre': main.vendedor.nombreApellido})
		trabajo = OrdenDetalleModelForm()
		formset = fotos(instance=main, prefix="fotos")
	return render(request, "ordenes/form2.html", {'form': form, 'formset': formset, 'trabajo': trabajo, 'main': main,
												  'permisos': permisos, 'especialidad': especialidad,
												  'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'area': area, 'estado': estado})


@permission_required('ordenes.change_ordentrabajo', raise_exception=True)
def recepcionarTrabajo(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	main = OrdenTrabajo.objects.get(pk=pk)
	main.modificado_por = request.user
	main.modificado_el = timezone.now()
	main.estado = "PEDIDO CONFIRMADO"
	main.save()
	trabajos = OrdenDetalle.objects.filter(orden=main)
	for t in trabajos:
		t.estado = "PREPARADOR BANDEJA ENTRADA"
		t.area = "YESO"
		t.save()
		e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main, trabajo=t,
																 estado="Se confirma el trabajo.",
																 area="CARGA INICIAL",
																 usuario=request.user)
		e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main, trabajo=t,
																	 estado="La orden pasa a insumos.",
																	 area="YESO",
																	 usuario=request.user)
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main,
																 estado="PEDIDO CONFIRMADO")
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area) + '&estado=' + str(estado))


@permission_required('ordenes.view_ordentrabajo', raise_exception=True)
def OrdenTrabajoListView(request):
	l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
	permisos = list(l)
	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	form = BuscadorOrdenes(initial={'especialidad': especialidad, 'clinicaExterna': clinica,
									'tipoTrabajo': tipoTrabajo, 'paciente': paciente,
									'desde': desde, 'hasta': hasta, 'odontos': odontos,
									'particulares': particulares,'area': area, 'estado': estado})

	if len(permisos)>0:
		if permisos[0] == "Supervisor Tecnico":
			form = BuscadorOrdenesSupervisor(initial={'especialidad': especialidad, 'clinicaExterna': clinica,
													  'tipoTrabajo': tipoTrabajo, 'paciente': paciente,
													  'desde': desde, 'hasta': hasta, 'odontos': odontos,
													  'particulares': particulares, 'insumos': insumos})
		elif permisos[0] == "Vendedores":
			form = BuscadorOrdenesVendedores()
		data_context = {'request': request, 'permiso': permisos[0], 'form': form,
						'especialidad': especialidad, 'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
						'paciente': paciente, 'desde': desde, 'hasta': hasta, 'odontos': odontos,
					  'particulares': particulares, 'insumos': insumos, 'area': area, 'estado': estado}
	else:
		data_context = {'request': request, 'permiso': None, 'form': form}
	return render(request, 'ordenes/list.html', data_context)


permission_required('core.view_ordentrabajo', raise_exception=True)
def OrdenTrabajoHistorialListView(request, pk):
	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if hasta == "null":
		hasta = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	orden = OrdenDetalle.objects.get(pk=pk)
	data_context = {'request': request, 'pk': pk, 'orden': orden, 'history': orden.orden.history.all(),
					'especialidad': especialidad, 'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'estado':estado, 'area':area}
	return render(request, 'ordenes/list1.html', data_context)


class OrdenTrabajoDeleteView(DeleteView):
	model = OrdenTrabajo
	template_name = 'ordenes/delete.html'
	success_url = reverse_lazy('orden_list')

	@method_decorator(permission_required('ordenes.delete_ordentrabajo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(OrdenTrabajoDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):

		especialidad = request.GET.get('especialidad', None)
		clinica = request.GET.get('clinica', None)
		tipoTrabajo = request.GET.get('tipoTrabajo', None)
		paciente = request.GET.get('paciente', None)
		desde = request.GET.get('desde', None)
		hasta = request.GET.get('hasta', None)
		particulares = request.GET.get('particulares', None)
		odontos = request.GET.get('odontos', None)
		area = request.GET.get('area', None)
		estado = request.GET.get('estado', None)

		if especialidad == "null":
			especialidad = ''
		if clinica == "null":
			clinica = ''
		if tipoTrabajo == "null":
			tipoTrabajo = ''
		if paciente == "null":
			paciente = ''
		if desde == "null":
			desde = ''
		if hasta == "null":
			hasta = ''
		if area == "null":
			area = ''
		if estado == "null":
			estado = ''
		if particulares == "True" or particulares == "true":
			particulares = True
		else:
			particulares = False
		if odontos == "True" or odontos == "true":
			odontos = True
		else:
			odontos = False

		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area)+'&estado='+str(estado))

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def vaciadoAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "INSUMO BANDEJA ENTRADA":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "INSUMO BANDEJA ENTRADA"
	trabajo.area = "INSUMOS"
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="Se realiza un vaciado del trabajo en yeso.",
																 area="INSUMOS",
																 usuario=request.user)
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo sale de yeso y pasa a la sección insumos.",
																 area="INSUMOS",
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area) + '&estado=' + str(estado))


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def pasarInsumosAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "INSUMO BANDEJA ENTRADA":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "INSUMO BANDEJA ENTRADA"
	trabajo.area = "INSUMOS"
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo sale de yeso y pasa a la sección insumos.",
																 area="INSUMOS",
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area) + '&estado=' + str(estado))


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def rechazarInsumosAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	main = OrdenDetalle.objects.get(pk=pk)
	if main.estado == "RECHAZADO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")

	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main.orden, trabajo=main,
																 estado="Rechazado por insumos.",
																 area="INSUMOS",
																 usuario=request.user)
	if request.method == "POST":
		form = OrdenesTrabajoEstadoModelForm(request.POST, request.FILES, instance=e)
		if form.is_valid():
			a = form.save()
			a.save()
			main.estado = "RECHAZADO"
			main.area = "INSUMOS"
			main.save()
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos))
	else:
		form = OrdenesTrabajoEstadoModelForm(instance=e)
	return render(request, 'ordenes/rechazo.html', {'request': request, 'form': form,
					'especialidad': especialidad, 'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos})


permission_required('core.view_ordentrabajo', raise_exception=True)
def InsumosOrdenListView(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	orden = OrdenDetalle.objects.get(pk=pk)
	l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
	permisos = list(l)
	data_context = {'request': request, 'pk': pk, 'orden': orden, 'permiso': permisos[0],
					'especialidad': especialidad, 'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'insumos': insumos, 'area': area, 'estado': estado}
	return render(request, 'ordenes/insumos.html', data_context)


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def pasarTecnicosAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "ENTREGADO A LABORATORIO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "ENTREGADO A LABORATORIO"
	trabajo.area = "TECNICOS"
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo sale de insumos y pasa a producción.",
																 area="TECNICOS",
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+'&insumos='+str(insumos))


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def asignarTecnicoAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	main = OrdenDetalle.objects.get(pk=pk)
	if main.estado == "TECNICO ASIGNADO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")

	if request.method == "POST":
		form = OrdenDetalleTecnicoModelForm(request.POST, request.FILES, instance=main)
		if form.is_valid():
			a = form.save()
			a.estado = "TECNICO ASIGNADO"
			a.area = "TECNICOS"
			a.save()
			e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=a.orden, trabajo=a,
																		 estado="Se asigno un tecnico al trabajo.",
																		 area="TECNICOS",
																		 usuario=request.user)
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+'&insumos='+str(insumos)+'&area='+str(area)+'&estado='+str(estado))
	else:
		form = OrdenDetalleTecnicoModelForm(instance=main)
	return render(request, 'ordenes/tecnico.html', {'request': request, 'form': form,
					'especialidad': especialidad, 'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'insumos': insumos, 'area': area, 'estado': estado})

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def iniciarAccion(request, pk, area, orden, user):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	areaf = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if areaf == "null":
		areaf = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "TRABAJO INICIADO" and trabajo.area == area:
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "TRABAJO INICIADO"
	trabajo.area = area
	trabajo.etapaActual = area
	trabajo.etapaOrden = orden
	trabajo.tecnico_id = user
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo inicio.",
																 area=area,
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+'&insumos='+str(insumos)+'&area='+str(areaf)+'&estado='+str(estado))

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def finalizarAccion(request, pk, area, orden):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	areaf = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if areaf == "null":
		areaf = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "TRABAJO FINALIZADO" and trabajo.area == area:
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "TRABAJO FINALIZADO"
	trabajo.area = area
	trabajo.etapaActual = area
	trabajo.etapaOrden = orden
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo ha sido finalizado por el técnico.",
																 area=area,
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+'&insumos='+str(insumos)+'&area='+str(areaf)+'&estado='+str(estado))

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def enviarAccion(request, pk, area, orden):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	areaf = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if areaf == "null":
		areaf = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "ENTREGADO A LABORATORIO" and trabajo.area == area:
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "ENTREGADO A LABORATORIO"
	trabajo.area = area
	trabajo.etapaActual = area
	trabajo.etapaOrden = orden
	trabajo.tecnico = None
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo sale de un sector y pasa a otro dentro de producción.",
																 area=area,
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+'&insumos='+str(insumos)+'&area='+str(areaf)+'&estado='+str(estado))

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def enviarLogisticaAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "PENDIENTE DE RETIRO/ENTREGA":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "PENDIENTE DE RETIRO/ENTREGA"
	trabajo.area = "LOGISTICA SALIDA"
	trabajo.tecnico = None
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo ha sido enviado a logística, "
																		"se aguarda su retiro o envío.",
																 area="LOGISTICA SALIDA",
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+'&insumos='+str(insumos))

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def entregaAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	main = OrdenDetalle.objects.get(pk=pk)
	if main.estado == "TRABAJO ENTREGADO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")

	if request.method == "POST":
		form = OrdenDetalleEntregaModelForm(request.POST, request.FILES, instance=main)
		if form.is_valid():
			a = form.save()
			a.estado = "TRABAJO ENTREGADO"
			a.area = "LOGISTICA SALIDA"
			a.save()
			e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=a.orden, trabajo=a,
																		 estado="El trabajo abandono las instalaciones de la empresa.",
																		 area="LOGISTICA SALIDA",
																		 usuario=request.user)
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area)+'&estado='+str(estado))
	else:
		form = OrdenDetalleEntregaModelForm(instance=main)
	return render(request, 'ordenes/entrega.html', {'request': request, 'form': form, 'especialidad': especialidad,
													'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'area': area, 'estado': estado})


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def entregaRechazoAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	main = OrdenDetalle.objects.get(pk=pk)
	if main.estado == "TRABAJO RECHAZADO ENTREGADO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")

	if request.method == "POST":
		form = OrdenDetalleEntregaModelForm(request.POST, request.FILES, instance=main)
		if form.is_valid():
			a = form.save()
			a.estado = "TRABAJO RECHAZADO ENTREGADO"
			a.area = "LOGISTICA SALIDA"
			a.save()
			e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=a.orden, trabajo=a,
																		 estado="El trabajo rechazado ha sido devuelto.",
																		 area="LOGISTICA SALIDA",
																		 usuario=request.user)
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area) + '&estado=' + str(estado))
	else:
		form = OrdenDetalleEntregaModelForm(instance=main)
	return render(request, 'ordenes/entrega.html', {'request': request, 'form': form, 'especialidad': especialidad,
													'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'area': area, 'estado': estado})


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def pausarInsumosAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	main = OrdenDetalle.objects.get(pk=pk)
	if main.estado == "PAUSADO EN INSUMO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")

	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main.orden, trabajo=main,
																 estado="Pausado por insumos.",
																 area="INSUMOS",
																 usuario=request.user)
	if request.method == "POST":
		form = OrdenesTrabajoEstadoPausarModelForm(request.POST, request.FILES, instance=e)
		if form.is_valid():
			a = form.save()
			a.save()
			main.estado = "PAUSADO EN INSUMO"
			main.area = "INSUMOS"
			main.save()
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area) + '&estado=' + str(estado))
	else:
		form = OrdenesTrabajoEstadoPausarModelForm(instance=e)
	return render(request, 'ordenes/pausa.html', {'request': request, 'form': form, 'especialidad': especialidad,
													'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'area': area, 'estado': estado})


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def continuarInsumosAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False

	trabajo = OrdenDetalle.objects.get(pk=pk)
	if trabajo.estado == "REANUDADO EN INSUMO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
	trabajo.estado = "REANUDADO EN INSUMO"
	trabajo.area = "INSUMOS"
	trabajo.save()
	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																 estado="El trabajo ha sido reanudado.",
																 area="INSUMOS",
																 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area) + '&estado=' + str(estado))

@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def rechazarProduccionAccion(request, pk):

	especialidad = request.GET.get('especialidad', None)
	clinica = request.GET.get('clinica', None)
	tipoTrabajo = request.GET.get('tipoTrabajo', None)
	paciente = request.GET.get('paciente', None)
	desde = request.GET.get('desde', None)
	hasta = request.GET.get('hasta', None)
	particulares = request.GET.get('particulares', None)
	odontos = request.GET.get('odontos', None)
	insumos = request.GET.get('insumos', None)
	area = request.GET.get('area', None)
	estado = request.GET.get('estado', None)

	if especialidad == "null":
		especialidad = ''
	if clinica == "null":
		clinica = ''
	if tipoTrabajo == "null":
		tipoTrabajo = ''
	if paciente == "null":
		paciente = ''
	if desde == "null":
		desde = ''
	if hasta == "null":
		hasta = ''
	if area == "null":
		area = ''
	if estado == "null":
		estado = ''
	if particulares == "True" or particulares == "true":
		particulares = True
	else:
		particulares = False
	if odontos == "True" or odontos == "true":
		odontos = True
	else:
		odontos = False
	if insumos == "True" or insumos == "true":
		insumos = True
	else:
		insumos = False

	main = OrdenDetalle.objects.get(pk=pk)

	if main.estado == "RECHAZADO":
		return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")

	e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=main.orden, trabajo=main,
																 estado="Rechazado por producción.",
																 area="INSUMOS",
																 usuario=request.user)
	if request.method == "POST":
		form = OrdenesTrabajoEstadoModelForm(request.POST, request.FILES, instance=e)
		if form.is_valid():
			a = form.save()
			a.save()
			main.estado = "RECHAZADO"
			main.area = "TECNICOS"
			main.save()
			return HttpResponseRedirect(reverse_lazy('orden_list')+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)+'&insumos='+str(insumos)
										+ '&area=' + str(area) + '&estado=' + str(estado))
	else:
		form = OrdenesTrabajoEstadoModelForm(instance=e)
	return render(request, 'ordenes/rechazo.html', {'request': request, 'form': form, 'especialidad': especialidad,
													'clinica': clinica, 'tipoTrabajo': tipoTrabajo,
					'paciente': paciente, 'desde': desde, 'hasta': hasta, 'particulares': particulares,
					'odontos': odontos, 'insumos': insumos, 'area': area, 'estado': estado})


@permission_required('ordenes.change_ordendetalle', raise_exception=True)
def etapasAccion(request, pk, etapa):
	trabajo = OrdenDetalle.objects.get(pk=pk)
	if etapa==1:
		if trabajo.estado == "PRODUCCION - ETAPA DISEÑO DIGITAL":
			return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
		trabajo.estado = "PRODUCCION - ETAPA DISEÑO DIGITAL"
		trabajo.area = "TECNICOS"
		trabajo.save()
		e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																	 estado="El trabajo se encuentra en la etapa de Diseño Digital.",
																	 area="TECNICOS",
																	 usuario=request.user)
	elif etapa == 2:
		if trabajo.estado == "PRODUCCION - ETAPA FRESADO":
			return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
		trabajo.estado = "PRODUCCION - ETAPA FRESADO"
		trabajo.area = "TECNICOS"
		trabajo.save()
		e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																	 estado="El trabajo se encuentra en la etapa de Fresado.",
																	 area="TECNICOS",
																	 usuario=request.user)
	elif etapa == 3:
		if trabajo.estado == "PRODUCCION - ETAPA MAQUILLAJE":
			return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
		trabajo.estado = "PRODUCCION - ETAPA MAQUILLAJE"
		trabajo.area = "TECNICOS"
		trabajo.save()
		e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																	 estado="El trabajo se encuentra en la etapa de Maquillaje.",
																	 area="TECNICOS",
																	 usuario=request.user)
	elif etapa == 4:
		if trabajo.estado == "PRODUCCION - ETAPA SINTERIZACION":
			return HttpResponse("EL TRABAJO YA SE ENCUENTRA CON ESTE ESTADO")
		trabajo.estado = "PRODUCCION - ETAPA SINTERIZACION"
		trabajo.area = "TECNICOS"
		trabajo.save()
		e, created = OrdenesTrabajoEstado.objects.get_or_create(orden=trabajo.orden, trabajo=trabajo,
																	 estado="El trabajo se encuentra en la etapa de Sinterizacion.",
																	 area="TECNICOS",
																	 usuario=request.user)
	return HttpResponseRedirect(reverse_lazy('orden_list'))


class OrdenDetalleSectorUpdateView(UpdateView):
	model = OrdenDetalle
	form_class = OrdenDetalleSectorModelForm
	success_url = reverse_lazy('orden_list')
	template_name = 'ordenes/sector.html'

	@method_decorator(permission_required('core.change_ordendetalle', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(OrdenDetalleSectorUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(OrdenDetalleSectorUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request

		especialidad = self.request.GET.get('especialidad', None)
		clinica = self.request.GET.get('clinica', None)
		tipoTrabajo = self.request.GET.get('tipoTrabajo', None)
		paciente = self.request.GET.get('paciente', None)
		desde = self.request.GET.get('desde', None)
		hasta = self.request.GET.get('hasta', None)
		particulares = self.request.GET.get('particulares', None)
		odontos = self.request.GET.get('odontos', None)

		if especialidad == "null":
			especialidad = ''
		if clinica == "null":
			clinica = ''
		if tipoTrabajo == "null":
			tipoTrabajo = ''
		if paciente == "null":
			paciente = ''
		if desde == "null":
			desde = ''
		if hasta == "null":
			hasta = ''
		if particulares == "True" or particulares == "true":
			particulares = True
		else:
			particulares = False
		if odontos == "True" or odontos == "true":
			odontos = True
		else:
			odontos = False

		context['especialidad'] = especialidad
		context['clinica'] = clinica
		context['tipoTrabajo'] = tipoTrabajo
		context['paciente'] = paciente
		context['desde'] = desde
		context['hasta'] = hasta
		context['particulares'] = particulares
		context['odontos'] = odontos

		return context

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['tipo_trabajo'] = self.object.trabajo.tipoTrabajo
		return kwargs

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		# Obtener el tipo de trabajo correspondiente al trabajo de la orden
		tipo_trabajo = self.object.trabajo
		kwargs['tipo_trabajo'] = tipo_trabajo
		return kwargs

	def form_valid(self, form):

		especialidad = self.request.GET.get('especialidad', None)
		clinica = self.request.GET.get('clinica', None)
		tipoTrabajo = self.request.GET.get('tipoTrabajo', None)
		paciente = self.request.GET.get('paciente', None)
		desde = self.request.GET.get('desde', None)
		hasta = self.request.GET.get('hasta', None)
		particulares = self.request.GET.get('particulares', None)
		odontos = self.request.GET.get('odontos', None)
		area = self.request.GET.get('area', None)
		estado = self.request.GET.get('estado', None)

		if especialidad == "null":
			especialidad = ''
		if clinica == "null":
			clinica = ''
		if tipoTrabajo == "null":
			tipoTrabajo = ''
		if paciente == "null":
			paciente = ''
		if desde == "null":
			desde = ''
		if hasta == "null":
			hasta = ''
		if area == "null":
			area = ''
		if estado == "null":
			estado = ''
		if particulares == "True" or particulares == "true":
			particulares = True
		else:
			particulares = False
		if odontos == "True" or odontos == "true":
			odontos = True
		else:
			odontos = False

		self.object = form.save(commit=False)
		orden = TipoOrdenAreas.objects.get(tipoTrabajo=self.object.trabajo, area=self.object.etapaActual).orden
		self.object.etapaOrden = orden
		self.object.save()
		return HttpResponseRedirect(self.get_success_url()+'?especialidad='+str(especialidad)+'&clinica='+str(clinica)
										+'&tipoTrabajo='+str(tipoTrabajo)+'&paciente='+str(paciente)+'&desde='+str(desde)
										+'&hasta='+str(hasta)+'&particulares='+str(particulares)+'&odontos='+str(odontos)
										+ '&area=' + str(area)+'&estado='+str(estado))