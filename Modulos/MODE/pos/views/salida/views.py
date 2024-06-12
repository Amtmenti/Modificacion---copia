import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from core.pos.forms import RegistroSalidaForm
from core.pos.models import RegistroSalida
from core.security.mixins import GroupPermissionMixin

MODULE_NAME_SALIDA = 'Registro de Salidas'


class RegistroSalidaListView(GroupPermissionMixin, TemplateView):
    template_name = 'salida/list.html'
    permission_required = 'view_registrosalida'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in RegistroSalida.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registros de Salidas'
        context['list_url'] = reverse_lazy('salida_list')
        context['create_url'] = reverse_lazy('salida_create')
        context['module_name'] = MODULE_NAME_SALIDA
        return context


class RegistroSalidaCreateView(GroupPermissionMixin, CreateView):
    template_name = 'salida/create.html'
    model = RegistroSalida
    form_class = RegistroSalidaForm
    success_url = reverse_lazy('salida_list')
    permission_required = 'add_registrosalida'

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
        context['title'] = 'Nuevo registro de Salida'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME_SALIDA
        return context
