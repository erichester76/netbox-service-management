from netbox.views import generic
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.urls import reverse

from . import (
    filtersets, 
    forms, 
    tables
    )

from .models import (
    Solution, 
    ServiceTemplate, 
    ServiceTemplateGroup, 
    ServiceTemplateGroupComponent, 
    Service, 
    Component
)

from netbox.views import generic
from django.db import models

def generate_mermaid_diagram(self, instance):
    # Helper function to generate a Mermaid diagram string for the given instance.
    diagram = "graph TD\n"
    visited = set()

    def add_node(obj, parent_label=None):
        label = f"{obj._meta.model_name}_{obj.pk}"
        if label in visited:
            return
        visited.add(label)

        # Add the current object to the diagram
        diagram_line = f'{label}["{obj._meta.verbose_name}: {obj}"]'
        diagram += diagram_line + "\n"

        # Add an edge from the parent node if applicable
        if parent_label:
            diagram += f"{parent_label} --> {label}\n"

        # Process related objects recursively
        for rel in obj._meta.get_fields():
            if rel.is_relation and rel.auto_created and not rel.concrete:
                related_objects = getattr(obj, rel.get_accessor_name()).all()
                for related_obj in related_objects:
                    add_node(related_obj, label)

    # Start the diagram with the main object
    add_node(instance)

    return diagram

class BaseDetailView(generic.ObjectView):
    template_name = 'netbox_service_management/default-detail.html'
    
    def get_extra_context(self, request, instance):
        # Extract fields and their values for the object, including relationships
        field_data = []
        object_name = instance._meta.verbose_name
                # Define fields to exclude
        excluded_fields = {
            'id', 
            'custom_field_data', 
            'tags', 
            'bookmarks', 
            'journal_entries', 
            'subscriptions', 
            'tagged_items', 
            'service_templates',
            'stg_components',
            'components',
            'template_groups',
            'services',
            'depends_on',
            'dependencies',
            'created',
            'last_updated',
        }

        # Extract fields and their values for the object, including relationships
        field_data = []
        for field in instance._meta.get_fields():
            # Skip excluded fields
            if field.name in excluded_fields:
                continue
            
            value = None
            url = None
            try:
                # Handle many-to-many or one-to-many relationships
                if field.many_to_many or field.one_to_many:
                    related_objects = getattr(instance, field.name).all()
                    value = ", ".join([str(obj) for obj in related_objects])

                # Handle ForeignKey and OneToOne relationships
                elif isinstance(field, (ForeignKey, OneToOneField)):
                    related_object = getattr(instance, field.name)
                    value = str(related_object) if related_object else None
                    if hasattr(related_object, 'get_absolute_url'):
                        url = related_object.get_absolute_url()
                        
                # Handle regular fields
                else:
                    value = getattr(instance, field.name)
            except AttributeError:
                value = None  # In case the relationship doesn't exist or is optional

            field_data.append({
                'name': field.verbose_name if hasattr(field, 'verbose_name') else field.name,
                'value': value,
                'url': url,  
            })

        # Find reverse relations dynamically and add them to related_tables
        related_tables = []
        for rel in instance._meta.get_fields():
            if rel.is_relation and rel.auto_created and not rel.concrete:
                related_model = rel.related_model
                related_objects = getattr(instance, rel.get_accessor_name()).all() 
                if related_objects.exists():
                                    # Create the URL for adding a new related object
                    add_url = None
                    if hasattr(related_model, 'get_absolute_url'):
                        model_name = related_model._meta.model_name
                        add_url = reverse(
                            f'plugins:netbox_service_management:{model_name}_add'
                        )   
                        # Pre-fill the linking field with the current object's ID, if possible
                        add_url += f'?{instance._meta.model_name}={instance.pk}'

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
                        'add_url': add_url,
                    })
                    
        # Generate Mermaid diagram for the object and its related objects
        mermaid_diagram = self.generate_mermaid_diagram(instance)

        return {
            'object_name': object_name,
            'field_data': field_data,
            'related_tables': related_tables,
            'mermaid_diagram': mermaid_diagram,
        }
        

class SolutionDetailView(BaseDetailView):
    queryset = Solution.objects.all()
    table = tables.SolutionTable
    
class SolutionListView(generic.ObjectListView):
    queryset = Solution.objects.all()
    table = tables.SolutionTable

class SolutionEditView(generic.ObjectEditView):
    queryset = Solution.objects.all()
    form = forms.SolutionForm

class SolutionDeleteView(generic.ObjectDeleteView):
    queryset = Solution.objects.all()
    
class ServiceTemplateDetailView(BaseDetailView):
    queryset = ServiceTemplate.objects.all()

class ServiceTemplateListView(generic.ObjectListView):
    queryset = ServiceTemplate.objects.all()
    table = tables.ServiceTemplateTable

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = ServiceTemplate.objects.all()
    form = forms.ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplate.objects.all()

class ServiceTemplateGroupDetailView(BaseDetailView):
    queryset = ServiceTemplateGroup.objects.all()

class ServiceTemplateGroupListView(generic.ObjectListView):
    queryset = ServiceTemplateGroup.objects.all()
    table = tables.ServiceTemplateGroupTable

class ServiceTemplateGroupEditView(generic.ObjectEditView):
    queryset = ServiceTemplateGroup.objects.all()
    form = forms.ServiceTemplateGroupForm

class ServiceTemplateGroupDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplateGroup.objects.all()

class ServiceTemplateGroupComponentDetailView(BaseDetailView):
    queryset = ServiceTemplateGroupComponent.objects.all()

class ServiceTemplateGroupComponentListView(generic.ObjectListView):
    queryset = ServiceTemplateGroupComponent.objects.all()
    table = tables.ServiceTemplateGroupComponentTable

class ServiceTemplateGroupComponentEditView(generic.ObjectEditView):
    queryset = ServiceTemplateGroupComponent.objects.all()
    form = forms.ServiceTemplateGroupComponentForm

class ServiceTemplateGroupComponentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplateGroupComponent.objects.all()

class ServiceDetailView(BaseDetailView):
    queryset = Service.objects.all()

class ServiceListView(generic.ObjectListView):
    queryset = Service.objects.all()
    table = tables.ServiceTable

class ServiceEditView(generic.ObjectEditView):
    queryset = Service.objects.all()
    form = forms.ServiceForm

class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = Service.objects.all()

class ComponentDetailView(BaseDetailView):
    queryset = Component.objects.all()

class ComponentListView(generic.ObjectListView):
    queryset = Component.objects.all()
    table = tables.ComponentTable

class ComponentEditView(generic.ObjectEditView):
    queryset = Component.objects.all()
    form = forms.ComponentForm

class ComponentDeleteView(generic.ObjectDeleteView):
    queryset = Component.objects.all()

