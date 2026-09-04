from django.urls import path, include

from core.views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, tablero, \
	TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView, EspecialidadListView, EspecialidadCreateView, \
	EspecialidadUpdateView, EspecialidadDeleteView, FaseEspecialidadListView, FaseTareaView, TipoTrabajoListView, \
	TipoTrabajoCreateView, TipoTrabajoUpdateView, TipoTrabajoDeleteView, InsumoListView, InsumoCreateView, \
	InsumoUpdateView, InsumoDeleteView, MaterialListView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView, \
	MarcaColorListView, MarcaColorCreateView, MarcaColorUpdateView, MarcaColorDeleteView, CiudadListView, \
	CiudadCreateView, CiudadUpdateView, CiudadDeleteView, VendedorListView, VendedorCreateView, VendedorUpdateView, \
	VendedorDeleteView, SucursalListView, SucursalCreateView, SucursalUpdateView, SucursalDeleteView, PacienteListView, \
	PacienteCreateView, PacienteUpdateView, PacienteDeleteView, InsumosTrabajoView

urlpatterns = [
	path(r'tablero', tablero, name='tablero'),

	path(r'categoria/list', CategoriaListView, name='categoria_list'),
	path(r'categoria/create', CategoriaCreateView.as_view(), name='categoria_create'),
	path(r'categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
	path(r'categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),

	path(r'tarea/list', TareaListView, name='tarea_list'),
	path(r'tarea/create', TareaCreateView.as_view(), name='tarea_create'),
	path(r'tarea/update/<int:pk>/', TareaUpdateView.as_view(), name='tarea_update'),
	path(r'tarea/delete/<int:pk>/', TareaDeleteView.as_view(), name='tarea_delete'),

	path(r'especialidad/list', EspecialidadListView, name='especialidad_list'),
	path(r'especialidad/create', EspecialidadCreateView, name='especialidad_create'),
	path(r'especialidad/update/<int:pk>/', EspecialidadUpdateView, name='especialidad_update'),
	path(r'especialidad/delete/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad_delete'),
	path(r'especialidad/fase/<int:pk>/', FaseEspecialidadListView, name='especialidad_fase'),
	path(r'especialidad/fase_add/<int:pk>/', FaseTareaView, name='especialidad_fase_add'),

	path(r'tipotrabajo/list', TipoTrabajoListView, name='ttrabajo_list'),
	path(r'tipotrabajo/create', TipoTrabajoCreateView, name='ttrabajo_create'),
	path(r'tipotrabajo/update/<int:pk>/', TipoTrabajoUpdateView, name='ttrabajo_update'),
	path(r'tipotrabajo/delete/<int:pk>/', TipoTrabajoDeleteView.as_view(), name='ttrabajo_delete'),
	path(r'tipotrabajo/insumos/<int:pk>/', InsumosTrabajoView, name='ttrabajo_insumos'),

	path(r'insumo/list', InsumoListView, name='insumo_list'),
	path(r'insumo/create', InsumoCreateView.as_view(), name='insumo_create'),
	path(r'insumo/update/<int:pk>/', InsumoUpdateView.as_view(), name='insumo_update'),
	path(r'insumo/delete/<int:pk>/', InsumoDeleteView.as_view(), name='insumo_delete'),

	path(r'material/list', MaterialListView, name='material_list'),
	path(r'material/create', MaterialCreateView.as_view(), name='material_create'),
	path(r'material/update/<int:pk>/', MaterialUpdateView.as_view(), name='material_update'),
	path(r'material/delete/<int:pk>/', MaterialDeleteView.as_view(), name='material_delete'),

	path(r'marca/list', MarcaColorListView, name='marcar_list'),
	path(r'marca/create', MarcaColorCreateView, name='marca_create'),
	path(r'marca/update/<int:pk>/', MarcaColorUpdateView, name='marca_udpate'),
	path(r'marca/delete/<int:pk>/', MarcaColorDeleteView.as_view(), name='marca_delete'),

	path(r'ciudad/list', CiudadListView, name='ciudad_list'),
	path(r'ciudad/create', CiudadCreateView.as_view(), name='ciudad_create'),
	path(r'ciudad/update/<int:pk>/', CiudadUpdateView.as_view(), name='ciudad_update'),
	path(r'ciudad/delete/<int:pk>/', CiudadDeleteView.as_view(), name='ciudad_delete'),

	path(r'vendedor/list', VendedorListView, name='vendedor_list'),
	path(r'vendedor/create', VendedorCreateView.as_view(), name='vendedor_create'),
	path(r'vendedor/update/<int:pk>/', VendedorUpdateView.as_view(), name='vendedor_update'),
	path(r'vendedor/delete/<int:pk>/', VendedorDeleteView.as_view(), name='vendedor_delete'),

	path(r'sucursal/list', SucursalListView, name='sucursal_list'),
	path(r'sucursal/create', SucursalCreateView.as_view(), name='sucursal_create'),
	path(r'sucursal/update/<int:pk>/', SucursalUpdateView.as_view(), name='sucursal_update'),
	path(r'sucursal/delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursal_delete'),

	path(r'paciente/list', PacienteListView, name='paciente_list'),
	path(r'paciente/create', PacienteCreateView.as_view(), name='paciente_create'),
	path(r'paciente/update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
	path(r'paciente/delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),

]
