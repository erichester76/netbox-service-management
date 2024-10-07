from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables


class ServiceDetailView(generic.ObjectView):
    queryset = models.Service.objects.all()


class ServiceListView(generic.ObjectListView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable


class ServiceEditView(generic.ObjectEditView):
    queryset = models.Service.objects.all()
    form = forms.ServiceForm


class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = models.Service.objects.all()
