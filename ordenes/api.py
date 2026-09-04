import json

from django.contrib.auth.decorators import permission_required
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import TipoTrabajo, Especialidad
from ordenes.models import OrdenDetalle, OrdenesTrabajoEstado, OrdenTrabajo, MetodoRetiro
from ordenes.serializers import OrdenDetalleModelSerializer, OrdenesTrabajoEstadoModelSerializer, \
    MetodoRetiroModelsSerializer, OrdenDetalleAPIModelSerializer
from users.models import CustomUsers


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class MetodoRetiroAPIList(viewsets.ModelViewSet):
    queryset = MetodoRetiro.objects.filter(activo=True).order_by('descripcion')
    serializer_class = MetodoRetiroModelsSerializer


@permission_required('ordenes.add_ordentrabajo', raise_exception=True)
def get_met_trabajo(request, pk):
    tipo = TipoTrabajo.objects.get(pk=pk)
    return JsonResponse({'met': tipo.metodologiaTrabajo, 'dias': tipo.duracionEstimadaParticulares,
                         'dias5': tipo.duracionEstimadaParticulares5})

@ensure_csrf_cookie
@permission_required('ordenes.add_ordentrabajo', raise_exception=True)
def save_orden_trabajo(request):
    if request.method == 'POST':
        try:
            received_json_data = json.loads(request.body)
            print(received_json_data)
            if not received_json_data['id']:
                detalle = OrdenDetalle()
            else:
                detalle = OrdenDetalle.objects.get(pk=received_json_data['id'])
            detalle.orden_id = received_json_data['orden']
            detalle.express = received_json_data['express']
            detalle.categoria_id = received_json_data['categoria']
            detalle.trabajo_id = received_json_data['trabajo']
            detalle.color_id = received_json_data['color']
            detalle.dientes = received_json_data['dientes']
            detalle.maxilarSuperiorCompleto = received_json_data['maxilarSuperiorCompleto']
            detalle.maxilarInferiorCompleto = received_json_data['maxilarInferiorCompleto']
            detalle.fechaEntrega = received_json_data['fechaEntrega']
            detalle.modoEnvio = received_json_data['modoEnvio']
            detalle.observacion = received_json_data['observacion']
            detalle.creado_por_id = received_json_data['usuario']
            detalle.creado_el = timezone.now()
            detalle.estado = "NO CONFIRMADO"
            detalle.area = "CARGA INICIAL"
            detalle.save()
            OrdenDetalle.objects.filter(orden_id=received_json_data['orden'], categoria=None).delete()
            estado, created = OrdenesTrabajoEstado.objects.get_or_create(orden_id=received_json_data['orden'],
                                                                         trabajo=detalle,
                                                                         estado="Alta del trabajo en alta gama",
                                                                         area="CARGA INICIAL",
                                                                         usuario_id=received_json_data['usuario'])
            return JsonResponse({'data': 'OK'})
        except:
            return JsonResponse({'data': 'NOOK'})


@permission_required('ordenes.add_ordentrabajo', raise_exception=True)
def get_orden_trabajo(request, pk):
    trabajo = OrdenDetalle.objects.get(pk=pk)
    serializer = OrdenDetalleAPIModelSerializer(trabajo)
    return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)


@ensure_csrf_cookie
@permission_required('ordenes.change_ordentrabajo', raise_exception=True)
def change_orden_trabajo(request):
    if request.method == 'POST':
        try:
            received_json_data = json.loads(request.body)
            detalle = OrdenDetalle.objects.get(pk=received_json_data['id'])
            detalle.modificado_por_id = received_json_data['usuario']
            detalle.modificado_el = timezone.now()
            detalle.activo = False
            detalle.save()
            estado, created = OrdenesTrabajoEstado.objects.get_or_create(orden_id=received_json_data['orden'], trabajo=detalle,
                                                                         estado="Trabajo Borrado")
            return JsonResponse({'data': 'OK'})
        except:
            return JsonResponse({'data': 'NOOK'})


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenDetalleAPIList(viewsets.ModelViewSet):
    queryset = OrdenDetalle.objects.filter(activo=True).order_by('id')
    serializer_class = OrdenDetalleModelSerializer

    def get_queryset(self):
        #print(FaseEspecialidad.objects.filter(especialidad_id=self.kwargs.get('especialidad')))
        return OrdenDetalle.objects.filter(activo=True, orden_id=self.kwargs['orden']).exclude(categoria=None)

from django.db.models import Case, When

@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenAPIList(viewsets.ModelViewSet):
    queryset = OrdenDetalle.objects.filter(activo=True).order_by('id')
    serializer_class = OrdenDetalleModelSerializer

    def get_queryset(self):
        permisos = self.request.GET.get('permiso')

        qs = OrdenDetalle.objects.filter(activo=True, orden__activo=True)

        desde = self.request.GET.get('desde') #
        hasta = self.request.GET.get('hasta') #
        trabajo = self.request.GET.get('trabajo') #
        clinica = self.request.GET.get('clinica') #
        especialidad = self.request.GET.get('especialidad') #
        paciente = self.request.GET.get('paciente') #
        tipoTrabajo = self.request.GET.get('tipoTrabajo') #
        vendedor = self.request.GET.get('vendedor')
        particulares = self.request.GET.get('particulares')
        odontos = self.request.GET.get('odontos')
        area = self.request.GET.get('area')
        estado = self.request.GET.get('estado')

        print(type(particulares))
        print(particulares)
        print(odontos)
        print("estado",estado)
        print("area",area)

        if not desde == "" and not hasta == "":
            qs = qs.filter(orden__fechaSolicitud__range=[desde,hasta])
        if not trabajo == "":
            qs = qs.filter(pk=trabajo)
        if not clinica == "":
            qs = qs.filter(orden__clinicaExterna_id=clinica)
        if not especialidad == "":
            categoria = Especialidad.objects.get(pk=especialidad).categoria
            qs = qs.filter(categoria=categoria)
        if not paciente == "":
            qs = qs.filter(orden__paciente_id=paciente)
        if not tipoTrabajo == "":
            qs = qs.filter(trabajo_id=tipoTrabajo)
        if not estado == "":
            qs = qs.filter(estado=estado)
        if not area == "":
            qs = qs.filter(area=area)
        if particulares == "true":
            qs = qs.filter(orden__clinicaExterna__tipo='Clinica externa')
        if odontos == "true":
            qs = qs.filter(orden__clinicaExterna__tipo='Odontos')
        if permisos == "Logistica":
            qs = qs.exclude(estado__in=["TRABAJO ENTREGADO", "TRABAJO RECHAZADO ENTREGADO"])
            qs = qs.order_by('-id')
        elif permisos == "Vendedores":
            if not vendedor == "":
                qs = qs.filter(orden__vendedor_id=vendedor)
            qs = qs.order_by('-id')
        elif permisos == "Preparador":
            qs = qs.filter(estado="PREPARADOR BANDEJA ENTRADA")
            qs = qs.order_by('fechaEntrega')
        elif permisos == "Carga de insumos":
            qs = qs.filter(estado__in=["INSUMO BANDEJA ENTRADA", "PAUSADO EN INSUMO", "REANUDADO EN INSUMO"])
            qs = qs.order_by('fechaEntrega')
        elif permisos == "Supervisor Tecnico":
            usuario = self.request.GET.get('usuario')
            insumos = self.request.GET.get('insumos')
            user = CustomUsers.objects.get(pk=usuario)
            print(user.areas)
            print(qs)
            qs = qs.filter(
                Q(etapaActual__in=user.areas) |
                Q(etapaActual__isnull=True, trabajo__tipoordenareas__orden=1,
                  trabajo__tipoordenareas__area__in=user.areas)
            )
            if insumos == "true":
                qs = qs.filter(estado__in=["INSUMO BANDEJA ENTRADA", "PAUSADO EN INSUMO",
                                           "REANUDADO EN INSUMO"])
            else:
                qs = qs.filter(estado__in=["ENTREGADO A LABORATORIO","TECNICO ASIGNADO",
                                       "TRABAJO INICIADO","TRABAJO FINALIZADO"])
            qs = qs.order_by('fechaEntrega').distinct()
        elif permisos == "Tecnico":
            usuario = self.request.GET.get('usuario')
            user = CustomUsers.objects.get(pk=usuario)
            print(user.areas)
            qs = qs.filter(
                Q(etapaActual__in=user.areas) |
                Q(etapaActual__isnull=True, trabajo__tipoordenareas__orden=1,
                  trabajo__tipoordenareas__area__in=user.areas)
            )
            qs = qs.filter(Q(tecnico_id=int(usuario)) | Q(tecnico=None),estado__in=["ENTREGADO A LABORATORIO",
                                                                                    "TECNICO ASIGNADO",
                                       "TRABAJO INICIADO","TRABAJO FINALIZADO"])
            #qs = qs.order_by('fechaEntrega').distinct()
            qs = qs.annotate(
                order_by_state=Case(
                    When(estado="TRABAJO INICIADO", then=1),
                    When(estado="TRABAJO FINALIZADO", then=2),
                    default=3,
                    output_field=models.IntegerField(),
                ),
            ).order_by("order_by_state", "fechaEntrega").distinct()
        elif permisos == "Administrador":
            usuario = self.request.GET.get('usuario')
            qs = qs.exclude(categoria=None)
            qs = qs.exclude(estado__in=['COURIER ENTRANTE',''],trabajo=None).order_by('-orden__fechaSolicitud').distinct()
        return qs




@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenesTrabajoEstadoAPIList(viewsets.ModelViewSet):
    queryset = OrdenesTrabajoEstado.objects.all().order_by('id')
    serializer_class = OrdenesTrabajoEstadoModelSerializer

    def get_queryset(self):
        #print(FaseEspecialidad.objects.filter(especialidad_id=self.kwargs.get('especialidad')))
        return OrdenesTrabajoEstado.objects.filter(trabajo_id=self.kwargs['trabajo'])
