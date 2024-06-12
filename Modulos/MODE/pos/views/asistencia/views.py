import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView
from core.pos.forms import RegistroAsistenciaForm
from core.pos.models import RegistroAsistencia
from core.security.mixins import GroupPermissionMixin

MODULE_NAME = 'Registros de Asistencia'


class RegistroAsistenciaListView(GroupPermissionMixin, TemplateView):
    template_name = 'asistencia/list.html'
    permission_required = 'view_registroasistencia'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in RegistroAsistencia.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registros de Asistencia'
        context['list_url'] = reverse_lazy('asistencia_list')
        context['create_url'] = reverse_lazy('asistencia_create')
        context['module_name'] = MODULE_NAME
        return context


class RegistroAsistenciaCreateView(GroupPermissionMixin, CreateView):
    template_name = 'asistencia/create.html'
    model = RegistroAsistencia
    form_class = RegistroAsistenciaForm
    success_url = reverse_lazy('asistencia_list')
    permission_required = 'add_registroasistencia'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de Asistencia'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class RegistroAsistenciaUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'asistencia/create.html'
    model = RegistroAsistencia
    form_class = RegistroAsistenciaForm
    success_url = reverse_lazy('asistencia_list')
    permission_required = 'change_registroasistencia'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Registro de Asistencia'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class RegistroAsistenciaDeleteView(GroupPermissionMixin, DeleteView):
    model = RegistroAsistencia
    template_name = 'delete.html'
    success_url = reverse_lazy('asistencia_list')
    permission_required = 'delete_registroasistencia'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Registro de Asistencia'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context
