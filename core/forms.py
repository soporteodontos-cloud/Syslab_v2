from dal_select2.widgets import ModelSelect2
from django import forms

from core.models import Categoria, Tarea, Especialidad, FaseEspecialidad, FaseTarea, TipoTrabajo, Insumo, Material, \
    MarcaColor, ColorDetalle, Ciudad, Vendedor, Sucursal, Paciente, TrabajoInsumo, TipoOrdenAreas


class CategoriaModelForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = {'descripcion'}


class TareaModelForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = {'descripcion'}


class EspecialidadModelForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = {'descripcion', 'categoria'}
        widgets = {
            'categoria': ModelSelect2(url='categoria-autocomplete'),
        }


class FaseEspecialidadModelForm(forms.ModelForm):
    class Meta:
        model = FaseEspecialidad
        fields = {'especialidad','descripcion','rol'}
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control js-example-basic-single'})
        }


class TareaFaseEspecialidadModelForm(forms.ModelForm):
    class Meta:
        model = FaseEspecialidad
        fields = {'id'}
        widgets = {
            'id': forms.HiddenInput()
        }


class FaseTareaModelForm(forms.ModelForm):
    class Meta:
        model = FaseTarea
        fields = {'fase','tarea'}
        widgets = {
            'tarea': forms.Select(attrs={'class': 'form-control js-example-basic-single'})
        }


class TipoTrabajoModelForm(forms.ModelForm):

    class Meta:
        model = TipoTrabajo
        fields = {'descripcion', 'especialidad', 'metodologiaTrabajo', 'precio', 'duracionEstimadaOdontos',
                  'duracionEstimadaParticulares', 'duracionEstimadaOdontos5', 'duracionEstimadaParticulares5', 'minimoDientes', 'maximoDientes'}
        widgets = {
            'especialidad': ModelSelect2(url='especialidad-autocomplete'),
            'metodologiaTrabajo': forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
            'precio': forms.TextInput(attrs={'class': 'form-control entero'})
        }
    field_order = ['descripcion', 'especialidad', 'metodologiaTrabajo', 'precio', 'duracionEstimadaOdontos', 'duracionEstimadaOdontos5',
              'duracionEstimadaParticulares', 'duracionEstimadaParticulares5', 'minimoDientes', 'maximoDientes']


class InsumoModelForm(forms.ModelForm):
    class Meta:
        model = Insumo
        #fields = {'descripcion','tipo', 'cantidad'}
        fields = {'descripcion', 'tipo'}
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
            #'cantidad': forms.TextInput(attrs={'class': 'form-control decimal'})
        }

    #field_order = ['descripcion','tipo', 'cantidad']
    field_order = ['descripcion', 'tipo']


class MaterialModelForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = {'descripcion'}


class MarcaColorModelForm(forms.ModelForm):
    class Meta:
        model = MarcaColor
        fields = {'descripcion'}


class ColorDetalleModelForm(forms.ModelForm):
    class Meta:
        model = ColorDetalle
        fields = {'marca','codigo', 'descripcion'}
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CiudadModelForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = {'descripcion'}


class VendedorModelForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = {'nombreApellido', 'telefono', 'ruc', 'dv', 'email'}
    field_order = ['nombreApellido', 'telefono', 'ruc', 'dv', 'email']


class SucursalModelForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = {'tipo', 'descripcion', 'nombreClinica', 'razonSocial', 'telefono', 'ruc', 'dv', 'ciudad',
                  'direccion', 'email', 'vendedor'}
        widgets = {
            'ciudad': ModelSelect2(url='ciudad-autocomplete'),
            'vendedor': ModelSelect2(url='vendedor-autocomplete'),
        }
    field_order = ['tipo', 'descripcion', 'nombreClinica', 'razonSocial', 'telefono', 'ruc', 'dv', 'ciudad',
                  'direccion', 'email', 'vendedor']


class PacienteModelForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = {'nombreApellido', 'razonSocial', 'telefono', 'ruc', 'dv', 'ciudad',
                  'direccion', 'email'}
        widgets = {
            'ciudad': ModelSelect2(url='ciudad-autocomplete'),
        }
    field_order = ['nombreApellido', 'razonSocial', 'telefono', 'ruc', 'dv', 'ciudad',
                  'direccion', 'email']


class TrabajoInsumoModelForm(forms.ModelForm):
    class Meta:
        model = TrabajoInsumo
        fields = {'trabajo','insumo','cantidad'}
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
            # 'cantidad': forms.TextInput(attrs={'class': 'form-control decimal'})
        }


class InsumoTrabajoModelForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = {'id'}


class TipoOrdenAreasModelForm(forms.ModelForm):
    class Meta:
        model = TipoOrdenAreas
        fields = {'tipoTrabajo', 'orden', 'area'}