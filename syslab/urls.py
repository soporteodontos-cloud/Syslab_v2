"""syslab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers

from core.api import CategoriaAPIList, TareaAPIList, EspecialidadAPIList, EspecialidadFaseAPIList, TipoTrabajoAPIList, \
    InsumoAPIList, MaterialAPIList, MarcaColorAPIList, CiudadAPIList, VendedorAPIList, SucursalAPIList, PacienteAPIList, \
    TrabajoInsumoAPIList
from core.autocomplete import CategoriaAutocomplete, EspecialidadAutocomplete, CiudadAutocomplete, VendedorAutocomplete, \
    ClinicaExternaAutocomplete, VendedorFiltradoAutocomplete, PacienteAutocomplete
from informes.api import OrdenReporteAPIList, OrdenReporteEnProduccionAPIList, OrdenReporte2448APIList, \
    OrdenReporteEntregarAPIList
from ordenes.api import OrdenDetalleAPIList, OrdenAPIList, OrdenesTrabajoEstadoAPIList, MetodoRetiroAPIList
from ordenes.autocomplete import TipoTrabajoFiltradoAutocomplete, ColorDetalleAutocomplete, TipoTrabajoAutocomplete, \
    TecnicosAutocomplete, MetodoRetiroAutocomplete
from syslab import settings
from users.api import UsuariosPermisos, GruposPermisos, GruposUsuarios

router = routers.DefaultRouter()
router.register(r'cat-list-intra', CategoriaAPIList)
router.register(r'tar-list-intra', TareaAPIList)
router.register(r'esp-list-intra', EspecialidadAPIList)
router.register(r'fas-list-intra/(?P<especialidad>\d+)', EspecialidadFaseAPIList)
router.register(r'otr-list-intra/(?P<orden>\d+)', OrdenDetalleAPIList)
router.register(r'his-list-intra/(?P<trabajo>\d+)', OrdenesTrabajoEstadoAPIList)
router.register(r'itt-list-intra/(?P<trabajo>\d+)', TrabajoInsumoAPIList)
router.register(r'ord-list-intra', OrdenAPIList)
router.register(r'orp-list-intra', OrdenReporteAPIList)
router.register(r'orpp-list-intra', OrdenReporteEnProduccionAPIList)
router.register(r'orpv-list-intra', OrdenReporte2448APIList)
router.register(r'orpe-list-intra', OrdenReporteEntregarAPIList)
router.register(r'ttr-list-intra', TipoTrabajoAPIList)
router.register(r'ins-list-intra', InsumoAPIList)
router.register(r'mat-list-intra', MaterialAPIList)
router.register(r'mar-list-intra', MarcaColorAPIList)
router.register(r'ciu-list-intra', CiudadAPIList)
router.register(r'ven-list-intra', VendedorAPIList)
router.register(r'suc-list-intra', SucursalAPIList)
router.register(r'pac-list-intra', PacienteAPIList)
router.register(r'mer-list-intra', MetodoRetiroAPIList)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'usuario/permisos',
         UsuariosPermisos.as_view(), name="permisos_usuario_post"),
    path(r'grupo/permisos',
         GruposPermisos.as_view(), name="permisos_grupo_post"),
    path(r'grupo/usuarios',
         GruposUsuarios.as_view(), name="usuarios_grupo_post"),
    path('rest/', include(router.urls)),
    path('', include('core.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('informes/', include('informes.urls')),
    path('usuarios/', include('users.urls')),

    #Login, password & permissions
    path(r'', LoginView.as_view(), name='login'),
    path(r'password-change', PasswordChangeView.as_view(), name="password_change"),
    path(r'password-change-done', PasswordChangeDoneView.as_view(),
         {'template_name': 'registration/password_change_done.html'},
         name='password_change_done'),
    path(r'salir', LogoutView.as_view(), name="logout"),

    path(r'categoria-autocomplete', CategoriaAutocomplete.as_view(), name='categoria-autocomplete'),
    path(r'especialidad-autocomplete', EspecialidadAutocomplete.as_view(), name='especialidad-autocomplete'),
    path(r'ciudad-autocomplete', CiudadAutocomplete.as_view(), name='ciudad-autocomplete'),
    path(r'vendedor-autocomplete', VendedorAutocomplete.as_view(), name='vendedor-autocomplete'),
    path(r'clinica-autocomplete', ClinicaExternaAutocomplete.as_view(), name='clinica-autocomplete'),
    path(r'paciente-autocomplete', PacienteAutocomplete.as_view(), name='paciente-autocomplete'),
    path(r'vendedorfiltrado-autocomplete', VendedorFiltradoAutocomplete.as_view(), name='vendedorfiltrado-autocomplete'),
    path(r'tipotrabajofiltrado-autocomplete', TipoTrabajoFiltradoAutocomplete.as_view(), name='tipotrabajofiltrado-autocomplete'),
    path(r'tipotrabajo-autocomplete', TipoTrabajoAutocomplete.as_view(), name='tipotrabajo-autocomplete'),
    path(r'colordetalle-autocomplete', ColorDetalleAutocomplete.as_view(), name='colordetalle-autocomplete'),
	path(r'tecnicos-autocomplete', TecnicosAutocomplete.as_view(), name='tecnicos-autocomplete'),
    path(r'mretiro-autocomplete', MetodoRetiroAutocomplete.as_view(), name='mretiro-autocomplete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
