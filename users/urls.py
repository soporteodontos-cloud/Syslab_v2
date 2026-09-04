from django.urls import path

from users.views import CustomUsersListView, CustomUsersCreateView, CustomUsersUpdateView, EstadoUsuario, \
	CustomUsersPasswordResetView, PermisosUsuarios, GruposListView, GruposCreateView, GruposUpdateView, \
	GruposDeleteView, PermisosGrupos, UsuariosGrupos, CustomUsersAreasView

urlpatterns = [
	path(r'', CustomUsersListView.as_view(), name='listado_usuarios'),
	path(r'nuevo', CustomUsersCreateView.as_view(), name='agregar_usuarios'),
	path(r'editar/<int:pk>/', CustomUsersUpdateView.as_view(), name='editar_usuarios'),
	path(r'areas/<int:pk>/', CustomUsersAreasView.as_view(), name='areas_usuarios'),
	path(r'estado/<int:pk>/<str:estado>/', EstadoUsuario, name='estado_usuarios'),
	path(r'password/<int:pk>/', CustomUsersPasswordResetView.as_view(), name='resetpassword_usuarios'),
	path(r'permisos/<int:pk>/', PermisosUsuarios, name='permisos_usuarios'),

	path(r'grupos', GruposListView.as_view(), name='listado_grupos'),
	path(r'grupos/nuevo', GruposCreateView.as_view(), name='agregar_grupos'),
	path(r'grupos/editar/<int:pk>/', GruposUpdateView.as_view(), name='editar_grupos'),
	path(r'grupos/borrar/<int:pk>/', GruposDeleteView.as_view(), name='borrar_grupos'),
	path(r'grupos/permisos/<int:pk>/', PermisosGrupos, name='permisos_grupos'),
	path(r'grupos/usuarios/<int:pk>/', UsuariosGrupos, name='usuarios_grupos'),
]
