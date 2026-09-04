from django.db.models import Count
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from core.models import Especialidad
from ordenes.models import OrdenDetalle
from ordenes.serializers import OrdenDetalleModelSerializer, OrdenDetalleReporteModelSerializer
from datetime import date, timedelta



def getTrabajosPorArea(request):
    cdesde = request.GET.get('cdesde')
    chasta = request.GET.get('chasta')
    edesde = request.GET.get('edesde')
    ehasta = request.GET.get('ehasta')

    trabajos = OrdenDetalle.objects.filter(orden__fechaSolicitud__range=[cdesde, chasta])

    if not edesde == '' and not ehasta == '':
        trabajos = trabajos.filter(fechaEntrega__range=[edesde, ehasta])

    trabajos = trabajos.values_list('area').annotate(total=Count('pk')).order_by('total')
    data = []
    for t in trabajos:
        dato = {'area': t[0],
                'cantidad': t[1]}
        data.append(dato)

    return JsonResponse({'data': data})


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenReporteAPIList(viewsets.ModelViewSet):
    queryset = OrdenDetalle.objects.filter(activo=True).order_by('id')
    serializer_class = OrdenDetalleReporteModelSerializer

    def get_queryset(self):
        qs = OrdenDetalle.objects.filter(activo=True)

        cargaDesde = self.request.GET.get('cargaDesde')
        cargaHasta = self.request.GET.get('cargaHasta')
        entregaDesde = self.request.GET.get('entregaDesde')
        entregaHasta = self.request.GET.get('entregaHasta')
        trabajo = self.request.GET.get('trabajo')
        clinica = self.request.GET.get('clinica')
        especialidad = self.request.GET.get('especialidad')
        paciente = self.request.GET.get('paciente')
        tipoTrabajo = self.request.GET.get('tipoTrabajo')
        metodo = self.request.GET.get('metodo')
        area = self.request.GET.get('area')
        estado = self.request.GET.get('estado')

        print(cargaHasta)
        print(cargaDesde)
        print(entregaDesde)
        print(entregaHasta)
        print(trabajo)
        print(clinica)
        print("especialidad", len(especialidad), type(especialidad), especialidad)
        print(paciente)
        print(tipoTrabajo)
        print(metodo)
        print(estado)
        print(area)

        if not cargaDesde == "" and not cargaHasta == "":
            qs = qs.filter(orden__fechaSolicitud__range=[cargaDesde,cargaHasta])
        if not entregaDesde == "" and not entregaHasta == "":
            qs = qs.filter(fechaEntrega__range=[entregaDesde, entregaHasta])
        if not trabajo == "":
            qs = qs.filter(pk=trabajo)
        if not clinica in ["", "NaN"]:
            qs = qs.filter(orden__clinicaExterna_id=clinica)
        if not especialidad in ["", "NaN"]:
            categoria = Especialidad.objects.get(pk=especialidad).categoria
            qs = qs.filter(categoria=categoria)
        if not paciente in ["", "NaN"]:
            qs = qs.filter(orden__paciente_id=paciente)
        if not tipoTrabajo in ["", "NaN"]:
            qs = qs.filter(trabajo_id=tipoTrabajo)
        if not metodo == "":
            qs = qs.filter(orden__metodoEnvio=metodo)
        if not area == "":
            qs = qs.filter(area=area)
        if not estado == "":
            qs = qs.filter(estado=estado)
        qs = qs.order_by('fechaEntrega')
        return qs


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenReporteEnProduccionAPIList(viewsets.ModelViewSet):
    queryset = OrdenDetalle.objects.filter(activo=True).order_by('id')
    serializer_class = OrdenDetalleModelSerializer

    def get_queryset(self):
        qs = OrdenDetalle.objects.filter(activo=True, estado__in=["ENTREGADO A LABORATORIO","TECNICO ASIGNADO",
                                       "TRABAJO INICIADO","TRABAJO FINALIZADO"]).order_by('-fechaEntrega')

        cargaDesde = self.request.GET.get('cargaDesde')
        cargaHasta = self.request.GET.get('cargaHasta')
        entregaDesde = self.request.GET.get('entregaDesde')
        entregaHasta = self.request.GET.get('entregaHasta')
        trabajo = self.request.GET.get('trabajo')
        clinica = self.request.GET.get('clinica')
        especialidad = self.request.GET.get('especialidad')
        paciente = self.request.GET.get('paciente')
        tipoTrabajo = self.request.GET.get('tipoTrabajo')
        metodo = self.request.GET.get('metodo')

        print(cargaHasta)
        print(cargaDesde)
        print(entregaDesde)
        print(entregaHasta)
        print(trabajo)
        print(clinica)
        print("especialidad", len(especialidad), type(especialidad), especialidad)
        print(paciente)
        print(tipoTrabajo)
        print(metodo)

        if not cargaDesde == "" and not cargaHasta == "":
            qs = qs.filter(orden__fechaSolicitud__range=[cargaDesde,cargaHasta])
        if not entregaDesde == "" and not entregaHasta == "":
            qs = qs.filter(fechaEntrega__range=[entregaDesde, entregaHasta])
        if not trabajo == "":
            qs = qs.filter(pk=trabajo)
        if not clinica in ["", "NaN"]:
            qs = qs.filter(orden__clinicaExterna_id=clinica)
        if not especialidad in ["", "NaN"]:
            categoria = Especialidad.objects.get(pk=especialidad).categoria
            qs = qs.filter(categoria=categoria)
        if not paciente in ["", "NaN"]:
            qs = qs.filter(orden__paciente_id=paciente)
        if not tipoTrabajo in ["", "NaN"]:
            qs = qs.filter(trabajo_id=tipoTrabajo)
        if not metodo == "":
            qs = qs.filter(orden__metodoEnvio=metodo)
        qs = qs.order_by('fechaEntrega')
        return qs


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenReporte2448APIList(viewsets.ModelViewSet):
    queryset = OrdenDetalle.objects.filter(activo=True).order_by('id')
    serializer_class = OrdenDetalleModelSerializer

    def get_queryset(self):

        fecha_actual = date.today()

        # Calcular la fecha límite
        fecha_limite = fecha_actual + timedelta(days=2)

        qs = OrdenDetalle.objects.filter(activo=True, fechaEntrega__lte=fecha_limite).exclude(estado__in=[
            "PENDIENTE DE RETIRO/ENTREGA","TRABAJO ENTREGADO", "TRABAJO RECHAZADO ENTREGADO"
        ]).order_by('-fechaEntrega')

        cargaDesde = self.request.GET.get('cargaDesde')
        cargaHasta = self.request.GET.get('cargaHasta')
        entregaDesde = self.request.GET.get('entregaDesde')
        entregaHasta = self.request.GET.get('entregaHasta')
        trabajo = self.request.GET.get('trabajo')
        clinica = self.request.GET.get('clinica')
        especialidad = self.request.GET.get('especialidad')
        paciente = self.request.GET.get('paciente')
        tipoTrabajo = self.request.GET.get('tipoTrabajo')
        metodo = self.request.GET.get('metodo')

        print(cargaHasta)
        print(cargaDesde)
        print(entregaDesde)
        print(entregaHasta)
        print(trabajo)
        print(clinica)
        print("especialidad", len(especialidad), type(especialidad), especialidad)
        print(paciente)
        print(tipoTrabajo)
        print(metodo)

        if not cargaDesde == "" and not cargaHasta == "":
            qs = qs.filter(orden__fechaSolicitud__range=[cargaDesde,cargaHasta])
        if not entregaDesde == "" and not entregaHasta == "":
            qs = qs.filter(fechaEntrega__range=[entregaDesde, entregaHasta])
        if not trabajo == "":
            qs = qs.filter(pk=trabajo)
        if not clinica in ["", "NaN"]:
            qs = qs.filter(orden__clinicaExterna_id=clinica)
        if not especialidad in ["", "NaN"]:
            categoria = Especialidad.objects.get(pk=especialidad).categoria
            qs = qs.filter(categoria=categoria)
        if not paciente in ["", "NaN"]:
            qs = qs.filter(orden__paciente_id=paciente)
        if not tipoTrabajo in ["", "NaN"]:
            qs = qs.filter(trabajo_id=tipoTrabajo)
        if not metodo == "":
            qs = qs.filter(orden__metodoEnvio=metodo)
        qs = qs.order_by('fechaEntrega')
        return qs


@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
class OrdenReporteEntregarAPIList(viewsets.ModelViewSet):
    queryset = OrdenDetalle.objects.filter(activo=True).order_by('id')
    serializer_class = OrdenDetalleModelSerializer

    def get_queryset(self):
        qs = OrdenDetalle.objects.filter(activo=True, estado__in=["PENDIENTE DE RETIRO/ENTREGA"]).order_by('-fechaEntrega')

        cargaDesde = self.request.GET.get('cargaDesde')
        cargaHasta = self.request.GET.get('cargaHasta')
        entregaDesde = self.request.GET.get('entregaDesde')
        entregaHasta = self.request.GET.get('entregaHasta')
        trabajo = self.request.GET.get('trabajo')
        clinica = self.request.GET.get('clinica')
        especialidad = self.request.GET.get('especialidad')
        paciente = self.request.GET.get('paciente')
        tipoTrabajo = self.request.GET.get('tipoTrabajo')
        metodo = self.request.GET.get('metodo')

        print(cargaHasta)
        print(cargaDesde)
        print(entregaDesde)
        print(entregaHasta)
        print(trabajo)
        print(clinica)
        print("especialidad", len(especialidad), type(especialidad), especialidad)
        print(paciente)
        print(tipoTrabajo)
        print(metodo)

        if not cargaDesde == "" and not cargaHasta == "":
            qs = qs.filter(orden__fechaSolicitud__range=[cargaDesde,cargaHasta])
        if not entregaDesde == "" and not entregaHasta == "":
            qs = qs.filter(fechaEntrega__range=[entregaDesde, entregaHasta])
        if not trabajo == "":
            qs = qs.filter(pk=trabajo)
        if not clinica in ["", "NaN"]:
            qs = qs.filter(orden__clinicaExterna_id=clinica)
        if not especialidad in ["", "NaN"]:
            categoria = Especialidad.objects.get(pk=especialidad).categoria
            qs = qs.filter(categoria=categoria)
        if not paciente in ["", "NaN"]:
            qs = qs.filter(orden__paciente_id=paciente)
        if not tipoTrabajo in ["", "NaN"]:
            qs = qs.filter(trabajo_id=tipoTrabajo)
        if not metodo == "":
            qs = qs.filter(orden__metodoEnvio=metodo)
        qs = qs.order_by('fechaEntrega')
        return qs