from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import Group
from core.models import Categoria, Tarea, Especialidad, FaseEspecialidad, TipoTrabajo, Insumo, Material, MarcaColor, \
    Ciudad, Vendedor, Sucursal, Paciente, ColorDetalle, TrabajoInsumo
from users.serializers import CustomUsersModelSerializer


class CategoriaModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = Categoria
        fields = ['id', 'descripcion', 'creado_por', 'creado_el']


class TareaModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = Tarea
        fields = ['id', 'descripcion', 'creado_por', 'creado_el']


class EspecialidadModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()
    categoria = CategoriaModelsSerializer()

    class Meta:
        model = Especialidad
        fields = ['id', 'descripcion', 'creado_por', 'creado_el', 'categoria']


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ['name']


class FaseEspecialidadModelSerializer(ModelSerializer):
    #especialidad = EspecialidadModelsSerializer()
    rol = GroupSerializer()

    class Meta:
        model = FaseEspecialidad
        fields = ['id', 'descripcion', 'rol', 'especialidad']


class TipoTrabajoModelSerializer(ModelSerializer):
    especialidad = EspecialidadModelsSerializer()
    creado_por = CustomUsersModelSerializer()


    class Meta:
        model = TipoTrabajo
        fields = ['id', 'descripcion', 'especialidad', 'metodologiaTrabajo', 'precio', 'duracionEstimadaOdontos',
                  'duracionEstimadaParticulares', 'minimoDientes', 'maximoDientes', 'creado_por', 'activo',
                  'modificado_por', 'creado_el', 'modificado_el']


class InsumoModelSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = Insumo
        fields = ['id', 'descripcion', 'tipo', 'creado_por', 'activo',
                  'modificado_por', 'creado_el', 'modificado_el']


class MaterialModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = Material
        fields = ['id', 'descripcion', 'creado_por', 'creado_el']


class MarcaColorModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = MarcaColor
        fields = ['id', 'descripcion', 'creado_por', 'creado_el']


class ColorDetalleModelsSerializer(ModelSerializer):
    marca = MarcaColorModelsSerializer()

    class Meta:
        model = ColorDetalle
        fields = ['id', 'marca', 'codigo', 'descripcion', 'creado_por', 'creado_el']


class CiudadModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = Ciudad
        fields = ['id', 'descripcion', 'creado_por', 'creado_el']


class VendedorModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = Vendedor
        fields = ['id', 'nombreApellido', 'telefono', 'ruc', 'dv', 'email', 'creado_por', 'creado_el']


class SucursalModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()
    vendedor = VendedorModelsSerializer()
    ciudad = CiudadModelsSerializer()

    class Meta:
        model = Sucursal
        fields = ['id', 'tipo', 'descripcion', 'nombreClinica', 'razonSocial', 'telefono', 'ruc', 'dv', 'ciudad',
                  'direccion', 'email', 'vendedor', 'creado_por', 'creado_el']


class PacienteModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()
    ciudad = CiudadModelsSerializer()

    class Meta:
        model = Paciente
        fields = ['id', 'nombreApellido', 'razonSocial', 'telefono', 'ruc', 'dv', 'ciudad',
                  'direccion', 'email', 'creado_por', 'creado_el']



class TrabajoInsumoModelSerializer(ModelSerializer):
    trabajo = TipoTrabajoModelSerializer()
    insumo = InsumoModelSerializer()

    class Meta:
        model = TrabajoInsumo
        fields = ['id', 'trabajo', 'insumo', 'cantidad']


