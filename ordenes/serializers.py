from django.utils import timezone
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.models import TipoOrdenAreas
from core.serializers import CategoriaModelsSerializer, ColorDetalleModelsSerializer, TipoTrabajoModelSerializer, \
    SucursalModelsSerializer, PacienteModelsSerializer, VendedorModelsSerializer
from ordenes.models import OrdenDetalle, OrdenTrabajo, OrdenesTrabajoEstado, MetodoRetiro
from users.serializers import CustomUsersModelSerializer


class MetodoRetiroModelsSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()

    class Meta:
        model = MetodoRetiro
        fields = ['id', 'descripcion', 'creado_por', 'creado_el']


class OrdenTrabajoModelSerializer(ModelSerializer):
    metodoEnvio = SerializerMethodField()
    clinicaExterna = SucursalModelsSerializer()
    paciente = PacienteModelsSerializer()
    creado_por = CustomUsersModelSerializer()
    vendedor = VendedorModelsSerializer()


    class Meta:
        model = OrdenTrabajo
        fields = ['id', 'fechaSolicitud', 'clinicaExterna', 'paciente', 'vendedor', 'observacion', 'estado', 'activo',
                  'creado_por', 'modificado_por', 'creado_el', 'envioCourrier', 'metodoEnvio', 'trabajoRepetido', 'vendedor']

    @staticmethod
    def get_metodoEnvio(obj):
        if obj.metodoEnvio == 'Ninguno':
            return '-'
        else:
            return obj.metodoEnvio



class OrdenDetalleModelSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()
    categoria = CategoriaModelsSerializer()
    color = ColorDetalleModelsSerializer()
    color_st = SerializerMethodField()
    trabajo = SerializerMethodField()
    #trabajo = TipoTrabajoModelSerializer()
    cantidad = SerializerMethodField()
    orden = OrdenTrabajoModelSerializer()
    odontologo = SerializerMethodField()
    dia_entrega = SerializerMethodField()
    can_etapas = SerializerMethodField()
    siguiente = SerializerMethodField()
    siguiente_etapa = SerializerMethodField()
    ultimo_cambio = SerializerMethodField()


    class Meta:
        model = OrdenDetalle
        fields = ['id', 'orden', 'express', 'categoria', 'trabajo', 'color', 'dientes', 'maxilarSuperiorCompleto',
                  'maxilarInferiorCompleto', 'fechaEntrega', 'modoEnvio', 'observacion', 'creado_por', 'creado_el',
				  'cantidad', 'estado', 'area', 'odontologo', 'dia_entrega', 'factura', 'color_st', 'etapaActual',
                  'etapaOrden', 'can_etapas', 'siguiente', 'siguiente_etapa', 'ultimo_cambio']

    @staticmethod
    def get_cantidad(obj):
        cant = len(obj.dientes)
        return cant

    @staticmethod
    def get_can_etapas(obj):
        cant = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).count()
        return cant

    @staticmethod
    def get_siguiente(obj):
        if obj.trabajo:
            if obj.etapaActual == None:
                etapa = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).order_by('orden')
                if etapa:
                    return etapa[0].orden
                else:
                    return None
            else:
                cant = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).count()
                if obj.etapaOrden < cant:
                    etapa = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo, orden__gt=obj.etapaOrden).order_by('orden')[0].orden
                    return etapa
                else:
                    return cant
        else:
            return None

    @staticmethod
    def get_siguiente_etapa(obj):
        if obj.trabajo:
            if obj.etapaActual == None:
                etapa = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).order_by('orden')
                if etapa:
                    return etapa[0].area
                else:
                    return None
            else:
                cant = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).count()
                if obj.etapaOrden < cant:
                    etapa = \
                    TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo, orden__gt=obj.etapaOrden).order_by('orden')[
                        0].area
                    return etapa
                else:
                    etapa = \
                    TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo, orden=obj.etapaOrden).order_by(
                            '-orden')[0].area
                    return etapa
        else:
            return None

    @staticmethod
    def get_odontologo(ob):
        return ''

    @staticmethod
    def get_trabajo(obj):
        if obj.trabajo:
            return obj.trabajo.descripcion
        else:
            return ''

    @staticmethod
    def get_dia_entrega(obj):
        if obj.fechaEntrega:
            delta = obj.fechaEntrega - timezone.now().date()
            return delta.days
        else:
            return -1

    @staticmethod
    def get_color_st(obj):
        if obj.color:
            return obj.color.descripcion
        else:
            return ''

    @staticmethod
    def get_ultimo_cambio(obj):
        ultimo = OrdenesTrabajoEstado.objects.filter(trabajo=obj).order_by('-id')
        if ultimo:
            return ultimo[0].fechaHora.strftime("%Y-%m-%d")
        return None


class OrdenDetalleReporteModelSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()
    categoria = CategoriaModelsSerializer()
    color = ColorDetalleModelsSerializer()
    color_st = SerializerMethodField()
    #trabajo = SerializerMethodField()
    trabajo = TipoTrabajoModelSerializer()
    cantidad = SerializerMethodField()
    orden = OrdenTrabajoModelSerializer()
    odontologo = SerializerMethodField()
    dia_entrega = SerializerMethodField()
    can_etapas = SerializerMethodField()
    siguiente = SerializerMethodField()
    siguiente_etapa = SerializerMethodField()
    ultimo_cambio = SerializerMethodField()


    class Meta:
        model = OrdenDetalle
        fields = ['id', 'orden', 'express', 'categoria', 'trabajo', 'color', 'dientes', 'maxilarSuperiorCompleto',
                  'maxilarInferiorCompleto', 'fechaEntrega', 'modoEnvio', 'observacion', 'creado_por', 'creado_el',
				  'cantidad', 'estado', 'area', 'odontologo', 'dia_entrega', 'factura', 'color_st', 'etapaActual',
                  'etapaOrden', 'can_etapas', 'siguiente', 'siguiente_etapa', 'ultimo_cambio']

    @staticmethod
    def get_cantidad(obj):
        cant = len(obj.dientes)
        return cant

    @staticmethod
    def get_can_etapas(obj):
        cant = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).count()
        return cant

    @staticmethod
    def get_siguiente(obj):
        if obj.trabajo:
            if obj.etapaActual == None:
                etapa = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).order_by('orden')
                if etapa:
                    return etapa[0].orden
                else:
                    return None
            else:
                cant = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).count()
                if obj.etapaOrden < cant:
                    etapa = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo, orden__gt=obj.etapaOrden).order_by('orden')[0].orden
                    return etapa
                else:
                    return cant
        else:
            return None

    @staticmethod
    def get_siguiente_etapa(obj):
        if obj.trabajo:
            if obj.etapaActual == None:
                etapa = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).order_by('orden')
                if etapa:
                    return etapa[0].area
                else:
                    return None
            else:
                cant = TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo).count()
                if obj.etapaOrden < cant:
                    etapa = \
                    TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo, orden__gt=obj.etapaOrden).order_by('orden')[
                        0].area
                    return etapa
                else:
                    etapa = \
                    TipoOrdenAreas.objects.filter(tipoTrabajo=obj.trabajo, orden=obj.etapaOrden).order_by(
                            '-orden')[0].area
                    return etapa
        else:
            return None

    @staticmethod
    def get_odontologo(ob):
        return ''

    @staticmethod
    def get_trabajo(obj):
        if obj.trabajo:
            return obj.trabajo.descripcion
        else:
            return ''

    @staticmethod
    def get_dia_entrega(obj):
        if obj.fechaEntrega:
            delta = obj.fechaEntrega - timezone.now().date()
            return delta.days
        else:
            return -1

    @staticmethod
    def get_color_st(obj):
        if obj.color:
            return obj.color.descripcion
        else:
            return ''

    @staticmethod
    def get_ultimo_cambio(obj):
        ultimo = OrdenesTrabajoEstado.objects.filter(trabajo=obj).order_by('-id')
        if ultimo:
            return ultimo[0].fechaHora.strftime("%Y-%m-%d")
        return None



class OrdenDetalleAPIModelSerializer(ModelSerializer):
    creado_por = CustomUsersModelSerializer()
    categoria = CategoriaModelsSerializer()
    color = ColorDetalleModelsSerializer()
    color_st = SerializerMethodField()
    #trabajo = SerializerMethodField()
    trabajo = TipoTrabajoModelSerializer()
    cantidad = SerializerMethodField()
    orden = OrdenTrabajoModelSerializer()
    odontologo = SerializerMethodField()
    dia_entrega = SerializerMethodField()

    class Meta:
        model = OrdenDetalle
        fields = ['id', 'orden', 'express', 'categoria', 'trabajo', 'color', 'dientes', 'maxilarSuperiorCompleto',
                  'maxilarInferiorCompleto', 'fechaEntrega', 'modoEnvio', 'observacion', 'creado_por', 'creado_el',
				  'cantidad', 'estado', 'area', 'odontologo', 'dia_entrega', 'factura', 'color_st']

    @staticmethod
    def get_cantidad(obj):
        cant = len(obj.dientes)
        return cant

    @staticmethod
    def get_odontologo(ob):
        return ''


    @staticmethod
    def get_dia_entrega(obj):
        if obj.fechaEntrega:
            delta = obj.fechaEntrega - timezone.now().date()
            return delta.days
        else:
            return -1

    @staticmethod
    def get_color_st(obj):
        if obj.color:
            return obj.color.descripcion
        else:
            return ''


class OrdenesTrabajoEstadoModelSerializer(ModelSerializer):
    orden = OrdenTrabajoModelSerializer()
    trabajo = OrdenDetalleModelSerializer()
    usuario = CustomUsersModelSerializer()


    class Meta:
        model = OrdenesTrabajoEstado
        fields = ['id', 'fechaHora', 'orden', 'trabajo', 'estado', 'area', 'usuario', 'motivo', 'imagen']


