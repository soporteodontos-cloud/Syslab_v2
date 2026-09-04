from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from core.models import Categoria, Tarea, Especialidad, FaseEspecialidad, TipoTrabajo, Insumo, Material, MarcaColor, \
    Ciudad, Vendedor, Sucursal, Paciente, TrabajoInsumo
from core.serializers import CategoriaModelsSerializer, TareaModelsSerializer, EspecialidadModelsSerializer, \
    FaseEspecialidadModelSerializer, TipoTrabajoModelSerializer, InsumoModelSerializer, MaterialModelsSerializer, \
    MarcaColorModelsSerializer, CiudadModelsSerializer, VendedorModelsSerializer, SucursalModelsSerializer, \
    PacienteModelsSerializer, TrabajoInsumoModelSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class CategoriaAPIList(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(activo=True).order_by('descripcion')
    serializer_class = CategoriaModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class TareaAPIList(viewsets.ModelViewSet):
    queryset = Tarea.objects.filter(activo=True).order_by('descripcion')
    serializer_class = TareaModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class EspecialidadAPIList(viewsets.ModelViewSet):
    queryset = Especialidad.objects.filter(activo=True).order_by('descripcion')
    serializer_class = EspecialidadModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class EspecialidadFaseAPIList(viewsets.ModelViewSet):
    queryset = FaseEspecialidad.objects.all().order_by('descripcion')
    serializer_class = FaseEspecialidadModelSerializer

    def get_queryset(self):
        #print(FaseEspecialidad.objects.filter(especialidad_id=self.kwargs.get('especialidad')))
        return FaseEspecialidad.objects.filter(especialidad_id=self.kwargs['especialidad'])


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class TipoTrabajoAPIList(viewsets.ModelViewSet):
    queryset = TipoTrabajo.objects.filter(activo=True).order_by('descripcion')
    serializer_class = TipoTrabajoModelSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class InsumoAPIList(viewsets.ModelViewSet):
    queryset = Insumo.objects.filter(activo=True).order_by('descripcion')
    serializer_class = InsumoModelSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class MaterialAPIList(viewsets.ModelViewSet):
    queryset = Material.objects.filter(activo=True).order_by('descripcion')
    serializer_class = MaterialModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class MarcaColorAPIList(viewsets.ModelViewSet):
    queryset = MarcaColor.objects.filter(activo=True).order_by('descripcion')
    serializer_class = MarcaColorModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class CiudadAPIList(viewsets.ModelViewSet):
    queryset = Ciudad.objects.filter(activo=True).order_by('descripcion')
    serializer_class = CiudadModelsSerializer

@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class VendedorAPIList(viewsets.ModelViewSet):
    queryset = Vendedor.objects.filter(activo=True).order_by('nombreApellido')
    serializer_class = VendedorModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class SucursalAPIList(viewsets.ModelViewSet):
    queryset = Sucursal.objects.filter(activo=True).order_by('descripcion')
    serializer_class = SucursalModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class PacienteAPIList(viewsets.ModelViewSet):
    queryset = Paciente.objects.filter(activo=True).order_by('nombreApellido')
    serializer_class = PacienteModelsSerializer


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class TrabajoInsumoAPIList(viewsets.ModelViewSet):
    queryset = TrabajoInsumo.objects.all().order_by('id')
    serializer_class = TrabajoInsumoModelSerializer

    def get_queryset(self):
        #print(FaseEspecialidad.objects.filter(especialidad_id=self.kwargs.get('especialidad')))
        return TrabajoInsumo.objects.filter(trabajo_id=self.kwargs['trabajo'])
