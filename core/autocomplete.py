from dal_select2.views import Select2QuerySetView
from django.db.models import Q

from core.models import Categoria, Especialidad, Vendedor, Ciudad, Sucursal, Paciente


class CategoriaAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = Categoria.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs


class EspecialidadAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = Especialidad.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs


class VendedorAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = Vendedor.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(nombreApellido__icontains=self.q)

        return qs


class CiudadAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = Ciudad.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs


class ClinicaExternaAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = Sucursal.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)

        return qs

#'poliza': ModelSelect2(url='poliza-autocomplete', forward=['asegurado']),
class VendedorFiltradoAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        clinica = self.forwarded.get('clinicaExterna', None)

        if clinica:

            sucursal = Sucursal.objects.get(pk=clinica)

            if sucursal.vendedor:
                qs = Vendedor.objects.filter(pk=sucursal.vendedor_id, activo=True)
        else:

            qs = Vendedor.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(nombreApellido__icontains=self.q)

        return qs


class PacienteAutocomplete(Select2QuerySetView):
    def get_queryset(self):

        qs = Paciente.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(Q(nombreApellido__icontains=self.q) | Q(ruc__icontains=self.q))

        return qs