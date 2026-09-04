from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.models import Permission, Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from users.forms import CustomUsersCreateModelForm, CustomUsersUpdateModelForm, CustomUsersPasswordResetModelForm, \
    CustomUsersAreasModelForm
from users.models import CustomUsers


class CustomUsersListView(ListView):
    model = CustomUsers
    template_name = 'registration/customusers_list.html'

    @method_decorator(permission_required('users.view_customusers', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CustomUsersListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return CustomUsers.objects.all()


class CustomUsersCreateView(CreateView):
    model = CustomUsers
    form_class = CustomUsersCreateModelForm
    template_name = 'registration/customusers_form.html'
    success_url = reverse_lazy('listado_usuarios')

    def get_context_data(self, **kwargs):
        context = super(CustomUsersCreateView, self).get_context_data(**kwargs)
        form = CustomUsersCreateModelForm()
        context['form'] = form
        return context

    @method_decorator(permission_required('users.add_customusers', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CustomUsersCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=True)
        object.set_password(object.password)
        object.save()
        return HttpResponseRedirect(self.success_url)


class CustomUsersUpdateView(UpdateView):
    model = CustomUsers
    form_class = CustomUsersUpdateModelForm
    template_name = 'registration/customusers_form.html'
    success_url = reverse_lazy('listado_usuarios')

    @method_decorator(permission_required('users.change_customusers', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CustomUsersUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CustomUsersUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomUsersUpdateView, self).get_context_data(**kwargs)
        form = CustomUsersUpdateModelForm(instance=context['object'])
        context['form'] = form
        return context

    def form_valid(self, form):
        object = form.save(commit=True)
        object.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        print(form.errors)


class CustomUsersAreasView(UpdateView):
    model = CustomUsers
    form_class = CustomUsersAreasModelForm
    template_name = 'registration/customusers_form.html'
    success_url = reverse_lazy('listado_usuarios')

    @method_decorator(permission_required('users.change_customusers', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CustomUsersAreasView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CustomUsersAreasView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomUsersAreasView, self).get_context_data(**kwargs)
        form = CustomUsersAreasModelForm(instance=context['object'])
        context['form'] = form
        return context

    def form_valid(self, form):
        object = form.save(commit=True)
        object.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        print(form.errors)


@permission_required('auth.change_customusers', raise_exception=True)
def EstadoUsuario(request, pk, estado):
    usuario = CustomUsers.objects.get(pk=pk)
    if estado == "A":
        usuario.is_active = True
    else:
        usuario.is_active = False
    usuario.save()
    return HttpResponseRedirect('/usuarios')


class CustomUsersPasswordResetView(UpdateView):
    model = CustomUsers
    form_class = CustomUsersPasswordResetModelForm
    template_name = 'registration/customusers_form.html'
    success_url = reverse_lazy('listado_usuarios')

    def get_initial(self):
        base_initial = super().get_initial()
        base_initial['password'] = ""
        return base_initial

    @method_decorator(permission_required('users.change_customusers', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CustomUsersPasswordResetView, self).dispatch(*args, **kwargs)

    def form_valid(self, CustomUsersPasswordResetView):
        object = CustomUsersPasswordResetView.save(commit=False)
        object.set_password(object.password)
        object.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CustomUsersPasswordResetView, self).get(request, *args, **kwargs)


@permission_required('users.change_customusers', raise_exception=True)
def PermisosUsuarios(request,pk):
    usuario = CustomUsers.objects.get(pk=pk)
    permisos_usuario = usuario.user_permissions.all()
    permisos = []

    aux1 = Permission.objects.all()

    for b in aux1:
        if b not in permisos_usuario:
            permisos.append(b)

    return render(request,
                 'registration/customusers_permisos.html',
                  {
                    'permisos': permisos,
                    'permisos_usuario': permisos_usuario,
                    'usuario': usuario,
                  })


class GruposListView(ListView):
    model = Group
    template_name = "registration/group_list.html"

    @method_decorator(permission_required('auth.view_group', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(GruposListView, self).dispatch(*args, **kwargs)


class GruposCreateView(CreateView):
    model = Group
    fields = {'name'}
    template_name = "registration/group_form.html"
    success_url = reverse_lazy('listado_grupos')

    @method_decorator(permission_required('auth.add_group', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(GruposCreateView, self).dispatch(*args, **kwargs)


class GruposUpdateView(UpdateView):
    model = Group
    fields = {'name'}
    template_name = "registration/group_form.html"
    success_url = reverse_lazy('listado_grupos')

    @method_decorator(permission_required('auth.change_group', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(GruposUpdateView, self).dispatch(*args, **kwargs)


class GruposDeleteView(DeleteView):
    model = Group
    template_name = "registration/group_confirm_delete.html"
    success_url = reverse_lazy('listado_grupos')

    @method_decorator(permission_required('auth.delete_group', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(GruposDeleteView, self).dispatch(*args, **kwargs)


@permission_required('auth.change_group', raise_exception=True)
def PermisosGrupos(request,pk):
    grupo = Group.objects.get(pk=pk)
    permisos_grupo = grupo.permissions.all()
    permisos = []

    aux1 = Permission.objects.all()

    for b in aux1:
        if b not in permisos_grupo:
            permisos.append(b)

    return render(request,
                 'registration/group_permisos.html',
                  {
                    'permisos': permisos,
                    'permisos_usuario': permisos_grupo,
                    'usuario': grupo,
                  })


@permission_required('auth.change_group', raise_exception=True)
def UsuariosGrupos(request,pk):

    grupo = Group.objects.get(pk=pk)
    usuarios_grupo = CustomUsers.objects.filter(groups=grupo)
    usuarios = []

    aux1 = CustomUsers.objects.filter(is_active=True)

    for b in aux1:
        if b not in usuarios_grupo:
            usuarios.append(b)

    data_context = {
        'request': request,
        'usuarios': usuarios,
        'usuarios_grupo': usuarios_grupo,
        'grupo': grupo,
    }
    return render(request, 'registration/group_users.html', data_context)