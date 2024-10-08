from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField


class SolutionDetailView(generic.ObjectView):
    queryset = models.Solution.objects.all()

    def get_extra_context(self, request, instance):
        related_tables = []
        # Loop over fields and identify relationships
        for field in instance._meta.get_fields():
            if field.is_relation:  # Check if the field is a relationship (FK, M2M, O2O)
                # Handle ManyToMany and Reverse ForeignKey relations
                if field.many_to_many or field.one_to_many:
                    related_objects = getattr(instance, field.name).all()
                # Handle ForeignKey and OneToOne relations
                elif isinstance(field, (ForeignKey, OneToOneField)):
                    related_objects = [getattr(instance, field.name)] if getattr(instance, field.name) else []

                related_tables.append({
                    'name': field.name,  # Name of the related field
                    'objects': related_objects,  # The related objects
                })

        return {
            'related_tables': related_tables,
        }

class SolutionListView(generic.ObjectListView):
    queryset = models.Solution.objects.all()
    table = tables.SolutionTable

class SolutionEditView(generic.ObjectEditView):
    queryset = models.Solution.objects.all()
    form = forms.SolutionForm

class SolutionDeleteView(generic.ObjectDeleteView):
    queryset = models.Solution.objects.all()
    
class ServiceTemplateDetailView(generic.ObjectView):
    queryset = models.ServiceTemplate.objects.all()

class ServiceTemplateListView(generic.ObjectListView):
    queryset = models.ServiceTemplate.objects.all()
    table = tables.ServiceTemplateTable

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplate.objects.all()
    form = forms.ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplate.objects.all()

class ServiceTemplateGroupDetailView(generic.ObjectView):
    queryset = models.ServiceTemplateGroup.objects.all()

class ServiceTemplateGroupListView(generic.ObjectListView):
    queryset = models.ServiceTemplateGroup.objects.all()
    table = tables.ServiceTemplateGroupTable

class ServiceTemplateGroupEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplateGroup.objects.all()
    form = forms.ServiceTemplateGroupForm

class ServiceTemplateGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplateGroup.objects.all()

class ServiceTemplateGroupComponentDetailView(generic.ObjectView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()

class ServiceTemplateGroupComponentListView(generic.ObjectListView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()
    table = tables.ServiceTemplateGroupComponentTable

class ServiceTemplateGroupComponentEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()
    form = forms.ServiceTemplateGroupComponentForm

class ServiceTemplateGroupComponentDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()

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

class ComponentDetailView(generic.ObjectView):
    queryset = models.Component.objects.all()

class ComponentListView(generic.ObjectListView):
    queryset = models.Component.objects.all()
    table = tables.ComponentTable

class ComponentEditView(generic.ObjectEditView):
    queryset = models.Component.objects.all()
    form = forms.ComponentForm

class ComponentDeleteView(generic.ObjectDeleteView):
    queryset = models.Component.objects.all()

