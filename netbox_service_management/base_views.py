import re
from django.contrib.contenttypes.fields import GenericForeignKey
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
            'object_id',
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
        mermaid_diagram = self.generate_mermaid_diagram(instance, max_depth=5)

        return {
            'object_name': object_name,
            'field_data': field_data,
            'related_tables': related_tables,
            'mermaid_diagram': mermaid_diagram,
        }

    def generate_mermaid_diagram(self, instance, max_depth=1):
        # Initialize the diagram string
        diagram = "graph TD\n"
        visited = set()
        processed_relationships = set()  # Track relationships to prevent circular references
        
        def sanitize_label(text):
            """Sanitize a text string to be used in a Mermaid node."""
            return re.sub(r'[^a-zA-Z0-9_]', '_', text)
        
        def add_node(obj, parent_label=None, current_depth=0):
            label = f"{sanitize_label(obj._meta.model_name)}_{obj.pk}"
            
            # Prevent circular reference by ensuring we don't revisit a node
            if label in visited or current_depth > max_depth:
                return
            visited.add(label)

            # Sanitize the object name for use in the diagram
            display_name = str(obj).replace('"', "'")  # Replace quotes to avoid breaking Mermaid syntax
            shape = f'{label}[({obj._meta.verbose_name}: {display_name})]'
            
            # Add the current object to the diagram
            nonlocal diagram
            diagram += shape + "\n"

            # Add a click event if the object has a URL
            if hasattr(obj, 'get_absolute_url'):
                diagram += f'click {label} "{obj.get_absolute_url()}"\n'

            # Add an edge from the parent node if applicable and avoid duplicates
            if parent_label and (parent_label, label) not in processed_relationships:
                diagram += f"{parent_label} --> {label}\n"
                processed_relationships.add((parent_label, label))

            # Define fields to skip (e.g., tags, problematic reverse relationships)
            excluded_fields = {'tags', 'datasource_set', 'custom_field_data', 'bookmarks', 'journal_entries', 'subscriptions'}

            # Process reverse relationships (auto-created relationships)
            for rel in obj._meta.get_fields():
                if rel.is_relation and rel.auto_created and not rel.concrete and rel.name not in excluded_fields:
                    if current_depth + 1 > max_depth:
                        continue
                    related_objects = getattr(obj, rel.get_accessor_name(), None)
                    if related_objects is not None and hasattr(related_objects, 'all'):
                        for related_obj in related_objects.all():
                            related_label = f"{sanitize_label(related_obj._meta.model_name)}_{related_obj.pk}"
                            if (related_label, label) not in processed_relationships:
                                add_node(related_obj, label, current_depth + 1)

             # Handle the specific relationship from Component to Service
            if isinstance(obj, Component) and obj.service:
                service = obj.service
                service_label = f"{sanitize_label(service._meta.model_name)}_{service.pk}"
                
                # Add the explicit link from Component to Service
                if (label, service_label) not in processed_relationships:
                    diagram += f"{service_label} --> {label}\n"
                    processed_relationships.add((label, service_label))
                
                # Continue processing relationships for Service, preserving its other connections
                add_node(service, label, current_depth)

            # Directly link the Service to its ServiceTemplate
            if isinstance(obj, Service) and obj.service_template:
                service_template = obj.service_template
                st_label = f"{sanitize_label(service_template._meta.model_name)}_{service_template.pk}"
                if (label, st_label) not in processed_relationships:
                    diagram += f"{st_label} --> {label}\n"
                    processed_relationships.add((label, st_label))
                    add_node(service_template, label, current_depth)

                                
        # Start the diagram with the main object
        add_node(instance)

        return diagram
