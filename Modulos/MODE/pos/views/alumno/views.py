import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView

from core.pos.forms import AlumnoForm
from core.pos.models import Alumno
from core.security.mixins import GroupPermissionMixin

MODULE_NAME = 'Alumnos'


class AlumnoListView(GroupPermissionMixin, TemplateView):
    template_name = 'alumno/list.html'
    permission_required = 'view_alumno'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Alumno.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Alumnos'
        context['list_url'] = reverse_lazy('alumno_list')
        context['create_url'] = reverse_lazy('alumno_create')
        context['module_name'] = MODULE_NAME
        return context


class AlumnoCreateView(GroupPermissionMixin, CreateView):
    template_name = 'alumno/create.html'
    model = Alumno
    form_class = AlumnoForm
    success_url = reverse_lazy('alumno_list')
    permission_required = 'add_alumno'

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
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Alumno'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class AlumnoUpdateView(GroupPermissionMixin, UpdateView):
    template_name = 'alumno/create.html'
    model = Alumno
    form_class = AlumnoForm
    success_url = reverse_lazy('alumno_list')
    permission_required = 'change_alumno'

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
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Alumno'
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class AlumnoDeleteView(GroupPermissionMixin, DeleteView):
    model = Alumno
    template_name = 'delete.html'
    success_url = reverse_lazy('alumno_list')
    permission_required = 'delete_alumno'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Alumno'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context