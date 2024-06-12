import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from core.pos.forms import RegistroEntradaForm
from core.pos.models import RegistroEntrada
from core.security.mixins import GroupPermissionMixin

MODULE_NAME_ENTRADA = 'Registro de Entradas'


class RegistroEntradaListView(GroupPermissionMixin, TemplateView):
    template_name = 'entrada/list.html'
    permission_required = 'view_registroentrada'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in RegistroEntrada.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registros de Entradas'
        context['list_url'] = reverse_lazy('entrada_list')
        context['create_url'] = reverse_lazy('entrada_create')
        context['module_name'] = MODULE_NAME_ENTRADA
        return context


class RegistroEntradaCreateView(GroupPermissionMixin, CreateView):
    template_name = 'entrada/create.html'
    model = RegistroEntrada
    form_class = RegistroEntradaForm
    success_url = reverse_lazy('entrada_list')
    permission_required = 'add_registroentrada'

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
        context['title'] = 'Nuevo registro de Entrada'
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME_ENTRADA
        return context
