from netbox.views import generic
from . import filtersets, forms, models, tables

from netbox.views import generic
from django.db import models

class BaseDetailView(generic.ObjectView):
    template_name = 'netbox_servicemanage_plugin/detail-default.html'
    
    def get_extra_context(self, request, instance):
        # Extract fields and their values for the object, including relationships
        field_data = []
        for field in instance._meta.get_fields():
            value = None
            try:
                # Handle many-to-many or one-to-many relationships
                if field.many_to_many or field.one_to_many:
                    related_objects = getattr(instance, field.name).all()
                    value = ", ".join([str(obj) for obj in related_objects])

                # Handle ForeignKey and OneToOne relationships
                elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
                    related_object = getattr(instance, field.name)
                    value = str(related_object) if related_object else None

                # Handle regular fields
                else:
                    value = getattr(instance, field.name)
            except AttributeError:
                value = None  # In case the relationship doesn't exist or is optional

            field_data.append({
                'name': field.verbose_name if hasattr(field, 'verbose_name') else field.name,
                'value': value,
            })

        # Find reverse relations dynamically and add them to related_tables
        related_tables = []
        for rel in instance._meta.get_fields():
            if rel.is_relation and rel.auto_created and not rel.concrete:
                related_model = rel.related_model
                related_objects = getattr(instance, rel.get_accessor_name()).all()
                
                if related_objects.exists():
                    # Create a table dynamically if a suitable one exists
                    table_class_name = f"{related_model.__name__}Table"
                    if hasattr(tables, table_class_name):
                        table_class = getattr(tables, table_class_name)
                        related_table = table_class(related_objects)
                    else:
                        related_table = None

                    related_tables.append({
                        'name': related_model._meta.verbose_name_plural,
                        'objects': related_objects,
                        'table': related_table,
                    })

        return {
            'field_data': field_data,
            'related_tables': related_tables,
        }

class SolutionDetailView(BaseDetailView):
    queryset = models.Solution.objects.all()
    table = tables.SolutionTable
    
class SolutionListView(generic.ObjectListView):
    queryset = models.Solution.objects.all()
    table = tables.SolutionTable

class SolutionEditView(generic.ObjectEditView):
    queryset = models.Solution.objects.all()
    form = forms.SolutionForm

class SolutionDeleteView(generic.ObjectDeleteView):
    queryset = models.Solution.objects.all()
    
class ServiceTemplateDetailView(BaseDetailView):
    queryset = models.ServiceTemplate.objects.all()

class ServiceTemplateListView(generic.ObjectListView):
    queryset = models.ServiceTemplate.objects.all()
    table = tables.ServiceTemplateTable

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplate.objects.all()
    form = forms.ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplate.objects.all()

class ServiceTemplateGroupDetailView(BaseDetailView):
    queryset = models.ServiceTemplateGroup.objects.all()

class ServiceTemplateGroupListView(generic.ObjectListView):
    queryset = models.ServiceTemplateGroup.objects.all()
    table = tables.ServiceTemplateGroupTable

class ServiceTemplateGroupEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplateGroup.objects.all()
    form = forms.ServiceTemplateGroupForm

class ServiceTemplateGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplateGroup.objects.all()

class ServiceTemplateGroupComponentDetailView(BaseDetailView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()

class ServiceTemplateGroupComponentListView(generic.ObjectListView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()
    table = tables.ServiceTemplateGroupComponentTable

class ServiceTemplateGroupComponentEditView(generic.ObjectEditView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()
    form = forms.ServiceTemplateGroupComponentForm

class ServiceTemplateGroupComponentDeleteView(generic.ObjectDeleteView):
    queryset = models.ServiceTemplateGroupComponent.objects.all()

class ServiceDetailView(BaseDetailView):
    queryset = models.Service.objects.all()

class ServiceListView(generic.ObjectListView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable

class ServiceEditView(generic.ObjectEditView):
    queryset = models.Service.objects.all()
    form = forms.ServiceForm

class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = models.Service.objects.all()

class ComponentDetailView(BaseDetailView):
    queryset = models.Component.objects.all()

class ComponentListView(generic.ObjectListView):
    queryset = models.Component.objects.all()
    table = tables.ComponentTable

class ComponentEditView(generic.ObjectEditView):
    queryset = models.Component.objects.all()
    form = forms.ComponentForm

class ComponentDeleteView(generic.ObjectDeleteView):
    queryset = models.Component.objects.all()

