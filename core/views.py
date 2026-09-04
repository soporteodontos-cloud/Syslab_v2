from django.contrib.auth.decorators import permission_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from core.forms import CategoriaModelForm, TareaModelForm, FaseEspecialidadModelForm, EspecialidadModelForm, \
	FaseTareaModelForm, TareaFaseEspecialidadModelForm, TipoTrabajoModelForm, InsumoModelForm, MaterialModelForm, \
	ColorDetalleModelForm, MarcaColorModelForm, CiudadModelForm, VendedorModelForm, SucursalModelForm, \
	PacienteModelForm, TrabajoInsumoModelForm, InsumoTrabajoModelForm, TipoOrdenAreasModelForm
from core.models import Categoria, Tarea, Especialidad, FaseEspecialidad, FaseTarea, TipoTrabajo, Insumo, Material, \
	MarcaColor, ColorDetalle, Ciudad, Vendedor, Sucursal, Paciente, TrabajoInsumo, TipoOrdenAreas


def tablero(request):

	return render(request, 'tablero.html', {
	})


@permission_required('core.view_categoria', raise_exception=True)
def CategoriaListView(request):
	data_context = {'request': request}
	return render(request, 'categoria/list.html', data_context)


class CategoriaCreateView(CreateView):
	model = Categoria
	form_class = CategoriaModelForm
	success_url = reverse_lazy('categoria_list')
	template_name = 'categoria/form.html'

	@method_decorator(permission_required('core.add_categoria', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CategoriaCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CategoriaCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class CategoriaUpdateView(UpdateView):
	model = Categoria
	form_class = CategoriaModelForm
	success_url = reverse_lazy('categoria_list')
	template_name = 'categoria/form.html'

	@method_decorator(permission_required('core.change_categoria', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CategoriaUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CategoriaUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class CategoriaDeleteView(DeleteView):
	model = Categoria
	template_name = 'categoria/delete.html'
	success_url = reverse_lazy('categoria_list')

	@method_decorator(permission_required('core.delete_categoria', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CategoriaDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_tarea', raise_exception=True)
def TareaListView(request):
	data_context = {'request': request}
	return render(request, 'tarea/list.html', data_context)


class TareaCreateView(CreateView):
	model = Tarea
	form_class = TareaModelForm
	success_url = reverse_lazy('tarea_list')
	template_name = 'tarea/form.html'

	@method_decorator(permission_required('core.add_tarea', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(TareaCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TareaCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class TareaUpdateView(UpdateView):
	model = Tarea
	form_class = TareaModelForm
	success_url = reverse_lazy('tarea_list')
	template_name = 'tarea/form.html'

	@method_decorator(permission_required('core.change_tarea', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(TareaUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TareaUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class TareaDeleteView(DeleteView):
	model = Tarea
	template_name = 'tarea/delete.html'
	success_url = reverse_lazy('tarea_list')

	@method_decorator(permission_required('core.delete_tarea', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(TareaDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_especialidad', raise_exception=True)
def EspecialidadListView(request):
	data_context = {'request': request}
	return render(request, 'especialidad/list.html', data_context)


@permission_required('core.add_especialidad', raise_exception=True)
def EspecialidadCreateView(request):
	main = Especialidad()
	main.creado_por = request.user
	main.creado_el = timezone.now()
	detalles = inlineformset_factory(Especialidad, FaseEspecialidad, form=FaseEspecialidadModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = EspecialidadModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('especialidad_list'))
	else:
		form = EspecialidadModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "especialidad/form.html", {'form': form, 'formset': formset})


@permission_required('core.change_especialidad', raise_exception=True)
def EspecialidadUpdateView(request, pk):
	main = Especialidad.objects.get(pk=pk)
	main.modificado_por = request.user
	main.modificado_el = timezone.now()
	detalles = inlineformset_factory(Especialidad, FaseEspecialidad, form=FaseEspecialidadModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = EspecialidadModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('especialidad_list'))
	else:
		form = EspecialidadModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "especialidad/form.html", {'form': form, 'formset': formset})


class EspecialidadDeleteView(DeleteView):
	model = Especialidad
	template_name = 'especialidad/delete.html'
	success_url = reverse_lazy('especialidad_list')

	@method_decorator(permission_required('core.delete_especialidad', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(EspecialidadDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_especialidad', raise_exception=True)
def FaseEspecialidadListView(request, pk):
	data_context = {'request': request, 'pk': pk}
	return render(request, 'especialidad/list1.html', data_context)


@permission_required('core.change_especialidad', raise_exception=True)
def FaseTareaView(request, pk):
	main = FaseEspecialidad.objects.get(pk=pk)
	detalles = inlineformset_factory(FaseEspecialidad, FaseTarea, form=FaseTareaModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = TareaFaseEspecialidadModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('especialidad_fase', kwargs={'pk': pk}))
	else:
		form = TareaFaseEspecialidadModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "especialidad/form1.html", {'form': form, 'formset': formset, 'main': main})


@permission_required('core.view_tipotrabajo', raise_exception=True)
def TipoTrabajoListView(request):
	data_context = {'request': request}
	return render(request, 'tipotrabajo/list.html', data_context)


# class TipoTrabajoCreateView(CreateView):
# 	model = TipoTrabajo
# 	form_class = TipoTrabajoModelForm
# 	success_url = reverse_lazy('ttrabajo_list')
# 	template_name = 'tipotrabajo/form.html'
#
# 	@method_decorator(permission_required('core.add_tipotrabajo', raise_exception=True))
# 	def dispatch(self, *args, **kwargs):
# 		return super(TipoTrabajoCreateView, self).dispatch(*args, **kwargs)
#
# 	def get_context_data(self, **kwargs):
# 		context = super(TipoTrabajoCreateView, self).get_context_data(**kwargs)
# 		context['request'] = self.request
# 		return context
#
# 	def form_valid(self, form):
# 		self.object = form.save(commit=False)
# 		self.object.creado_por = self.request.user
# 		self.object.creado_el = timezone.now()
# 		self.object.save()
# 		return HttpResponseRedirect(self.get_success_url())


def ordenes_correlativos(formset):
    ordenes = [int(form.cleaned_data.get('orden')) for form in formset]
    return ordenes == list(range(min(ordenes), max(ordenes) + 1))

@permission_required('core.add_tipotrabajo', raise_exception=True)
def TipoTrabajoCreateView(request):
	main = TipoTrabajo()
	main.creado_por = request.user
	main.creado_el = timezone.now()
	detalles = inlineformset_factory(TipoTrabajo, TipoOrdenAreas, form=TipoOrdenAreasModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = TipoTrabajoModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid() and ordenes_correlativos(formset):
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('ttrabajo_list'))
	else:
		form = TipoTrabajoModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "tipotrabajo/form.html", {'form': form, 'formset': formset, 'main': main})


@permission_required('core.change_tipotrabajo', raise_exception=True)
def TipoTrabajoUpdateView(request, pk):
	main = TipoTrabajo.objects.get(pk=pk)
	main.modificado_por = request.user
	main.modificado_el = timezone.now()
	detalles = inlineformset_factory(TipoTrabajo, TipoOrdenAreas, form=TipoOrdenAreasModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = TipoTrabajoModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid() and ordenes_correlativos(formset):
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('ttrabajo_list'))
	else:
		form = TipoTrabajoModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "tipotrabajo/form.html", {'form': form, 'formset': formset, 'main': main})


# class TipoTrabajoUpdateView(UpdateView):
# 	model = TipoTrabajo
# 	form_class = TipoTrabajoModelForm
# 	success_url = reverse_lazy('ttrabajo_list')
# 	template_name = 'tipotrabajo/form.html'
#
# 	@method_decorator(permission_required('core.change_tipotrabajo', raise_exception=True))
# 	def dispatch(self, *args, **kwargs):
# 		return super(TipoTrabajoUpdateView, self).dispatch(*args, **kwargs)
#
# 	def get_context_data(self, **kwargs):
# 		context = super(TipoTrabajoUpdateView, self).get_context_data(**kwargs)
# 		context['request'] = self.request
# 		return context
#
# 	def form_valid(self, form):
# 		self.object = form.save(commit=False)
# 		self.object.modificado_por = self.request.user
# 		self.object.modificado_el = timezone.now()
# 		self.object.save()
# 		return HttpResponseRedirect(self.get_success_url())


class TipoTrabajoDeleteView(DeleteView):
	model = TipoTrabajo
	template_name = 'tipotrabajo/delete.html'
	success_url = reverse_lazy('ttrabajo_list')

	@method_decorator(permission_required('core.delete_tipotrabajo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(TipoTrabajoDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_insumo', raise_exception=True)
def InsumoListView(request):
	data_context = {'request': request}
	return render(request, 'insumo/list.html', data_context)


class InsumoCreateView(CreateView):
	model = Insumo
	form_class = InsumoModelForm
	success_url = reverse_lazy('insumo_list')
	template_name = 'insumo/form.html'

	@method_decorator(permission_required('core.add_insumo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(InsumoCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(InsumoCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class InsumoUpdateView(UpdateView):
	model = Insumo
	form_class = InsumoModelForm
	success_url = reverse_lazy('insumo_list')
	template_name = 'insumo/form.html'

	@method_decorator(permission_required('core.change_insumo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(InsumoUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(InsumoUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class InsumoDeleteView(DeleteView):
	model = Insumo
	template_name = 'insumo/delete.html'
	success_url = reverse_lazy('insumo_list')

	@method_decorator(permission_required('core.delete_insumo', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(InsumoDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_material', raise_exception=True)
def MaterialListView(request):
	data_context = {'request': request}
	return render(request, 'material/list.html', data_context)


class MaterialCreateView(CreateView):
	model = Material
	form_class = MaterialModelForm
	success_url = reverse_lazy('material_list')
	template_name = 'material/form.html'

	@method_decorator(permission_required('core.add_material', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MaterialCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MaterialCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class MaterialUpdateView(UpdateView):
	model = Material
	form_class = MaterialModelForm
	success_url = reverse_lazy('material_list')
	template_name = 'material/form.html'

	@method_decorator(permission_required('core.change_material', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MaterialUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MaterialUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class MaterialDeleteView(DeleteView):
	model = Material
	template_name = 'material/delete.html'
	success_url = reverse_lazy('material_list')

	@method_decorator(permission_required('core.delete_material', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MaterialDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_marcacolor', raise_exception=True)
def MarcaColorListView(request):
	data_context = {'request': request}
	return render(request, 'marca/list.html', data_context)


@permission_required('core.add_marcacolor', raise_exception=True)
def MarcaColorCreateView(request):
	main = MarcaColor()
	main.creado_por = request.user
	main.creado_el = timezone.now()
	detalles = inlineformset_factory(MarcaColor, ColorDetalle, form=ColorDetalleModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = MarcaColorModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('marcar_list'))
	else:
		form = MarcaColorModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "marca/form.html", {'form': form, 'formset': formset, 'main': main})


@permission_required('core.change_marcacolor', raise_exception=True)
def MarcaColorUpdateView(request, pk):
	main = MarcaColor.objects.get(pk=pk)
	main.modificado_por = request.user
	main.modificado_el = timezone.now()
	detalles = inlineformset_factory(MarcaColor, ColorDetalle, form=ColorDetalleModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = MarcaColorModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('marcar_list'))
	else:
		form = MarcaColorModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "marca/form.html", {'form': form, 'formset': formset, 'main': main})


class MarcaColorDeleteView(DeleteView):
	model = MarcaColor
	template_name = 'marca/delete.html'
	success_url = reverse_lazy('marcar_list')

	@method_decorator(permission_required('core.delete_marcacolor', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MarcaColorDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_ciudad', raise_exception=True)
def CiudadListView(request):
	data_context = {'request': request}
	return render(request, 'ciudad/list.html', data_context)


class CiudadCreateView(CreateView):
	model = Ciudad
	form_class = CiudadModelForm
	success_url = reverse_lazy('ciudad_list')
	template_name = 'ciudad/form.html'

	@method_decorator(permission_required('core.add_ciudad', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CiudadCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CiudadCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class CiudadUpdateView(UpdateView):
	model = Ciudad
	form_class = CiudadModelForm
	success_url = reverse_lazy('ciudad_list')
	template_name = 'ciudad/form.html'

	@method_decorator(permission_required('core.change_ciudad', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CiudadUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CiudadUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class CiudadDeleteView(DeleteView):
	model = Ciudad
	template_name = 'ciudad/delete.html'
	success_url = reverse_lazy('ciudad_list')

	@method_decorator(permission_required('core.delete_ciudad', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CiudadDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_vendedor', raise_exception=True)
def VendedorListView(request):
	data_context = {'request': request}
	return render(request, 'vendedor/list.html', data_context)


class VendedorCreateView(CreateView):
	model = Vendedor
	form_class = VendedorModelForm
	success_url = reverse_lazy('vendedor_list')
	template_name = 'vendedor/form.html'

	@method_decorator(permission_required('core.add_vendedor', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(VendedorCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(VendedorCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class VendedorUpdateView(UpdateView):
	model = Vendedor
	form_class = VendedorModelForm
	success_url = reverse_lazy('vendedor_list')
	template_name = 'vendedor/form.html'

	@method_decorator(permission_required('core.change_vendedor', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(VendedorUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(VendedorUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class VendedorDeleteView(DeleteView):
	model = Vendedor
	template_name = 'vendedor/delete.html'
	success_url = reverse_lazy('vendedor_list')

	@method_decorator(permission_required('core.delete_vendedor', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(VendedorDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_sucursal', raise_exception=True)
def SucursalListView(request):
	data_context = {'request': request}
	return render(request, 'sucursal/list.html', data_context)


class SucursalCreateView(CreateView):
	model = Sucursal
	form_class = SucursalModelForm
	success_url = reverse_lazy('sucursal_list')
	template_name = 'sucursal/form.html'

	@method_decorator(permission_required('core.add_sucursal', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(SucursalCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(SucursalCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class SucursalUpdateView(UpdateView):
	model = Sucursal
	form_class = SucursalModelForm
	success_url = reverse_lazy('sucursal_list')
	template_name = 'sucursal/form.html'

	@method_decorator(permission_required('core.change_sucursal', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(SucursalUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(SucursalUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class SucursalDeleteView(DeleteView):
	model = Sucursal
	template_name = 'sucursal/delete.html'
	success_url = reverse_lazy('sucursal_list')

	@method_decorator(permission_required('core.delete_sucursal', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(SucursalDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.view_paciente', raise_exception=True)
def PacienteListView(request):
	data_context = {'request': request}
	return render(request, 'paciente/list.html', data_context)


class PacienteCreateView(CreateView):
	model = Paciente
	form_class = PacienteModelForm
	success_url = reverse_lazy('paciente_list')
	template_name = 'paciente/form.html'

	@method_decorator(permission_required('core.add_paciente', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(PacienteCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(PacienteCreateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creado_por = self.request.user
		self.object.creado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class PacienteUpdateView(UpdateView):
	model = Paciente
	form_class = PacienteModelForm
	success_url = reverse_lazy('paciente_list')
	template_name = 'paciente/form.html'

	@method_decorator(permission_required('core.change_paciente', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(PacienteUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(PacienteUpdateView, self).get_context_data(**kwargs)
		context['request'] = self.request
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class PacienteDeleteView(DeleteView):
	model = Paciente
	template_name = 'paciente/delete.html'
	success_url = reverse_lazy('paciente_list')

	@method_decorator(permission_required('core.delete_paciente', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(PacienteDeleteView, self).dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.activo = False
		self.object.modificado_por = self.request.user
		self.object.modificado_el = timezone.now()
		self.object.save()
		return HttpResponseRedirect(self.success_url)


@permission_required('core.add_tipotrabajo', raise_exception=True)
def InsumosTrabajoView(request, pk):
	main = TipoTrabajo.objects.get(pk=pk)
	main.creado_por = request.user
	main.creado_el = timezone.now()
	detalles = inlineformset_factory(TipoTrabajo, TrabajoInsumo, form=TrabajoInsumoModelForm, extra=1, can_delete=True)
	if request.method == "POST":
		form = InsumoTrabajoModelForm(request.POST, instance=main)
		formset = detalles(request.POST, instance=main, prefix="detalles")
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect(reverse_lazy('ttrabajo_list'))
	else:
		form = InsumoTrabajoModelForm(instance=main)
		formset = detalles(instance=main, prefix="detalles")
	return render(request, "tipotrabajo/insumos.html", {'form': form, 'formset': formset})