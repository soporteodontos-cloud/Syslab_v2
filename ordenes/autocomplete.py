from dal_select2.views import Select2QuerySetView
from django.db.models import Q

#'poliza': ModelSelect2(url='poliza-autocomplete', forward=['asegurado']),
from core.models import TipoTrabajo, ColorDetalle
from ordenes.models import MetodoRetiro
from users.models import CustomUsers


class MetodoRetiroAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = MetodoRetiro.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs

class TipoTrabajoAutocomplete(Select2QuerySetView):
    def get_queryset(self):


        qs = TipoTrabajo.objects.filter(activo=True)


        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs

class TipoTrabajoFiltradoAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        categoria = self.forwarded.get('categoria', None)

        print(categoria)

        a = TipoTrabajo.objects.all()
        for b in a:
            print(b.especialidad.categoria_id)

        qs = TipoTrabajo.objects.filter(especialidad__categoria_id=categoria, activo=True)


        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs


class ColorDetalleAutocomplete(Select2QuerySetView):


    def get_queryset(self):

        qs = ColorDetalle.objects.filter(marca__activo=True)


        if self.q:
            qs = qs.filter(Q(marca__descripcion__icontains=self.q) | Q(codigo__icontains=self.q))

        return qs


class TecnicosAutocomplete(Select2QuerySetView):


    def get_queryset(self):

        qs = CustomUsers.objects.filter(is_active=True, groups__name__in=['Tecnico'])


        if self.q:
            qs = qs.filter(Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q))

        return qs