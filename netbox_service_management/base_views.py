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
        mermaid_diagram = self.generate_mermaid_diagram(instance, max_depth=7)

        return {
            'object_name': object_name,
            'field_data': field_data,
            'related_tables': related_tables,
            'mermaid_diagram': mermaid_diagram,
        }

    def generate_mermaid_diagram(self, instance, max_depth=1):
        # Initialize the diagram string
        #diagram = "graph LR\n"
        visited = set()
        processed_relationships = set()  # Track relationships to prevent circular references
        
         # Define colors for each model type
        color_map = {
            'solution': '#D0E8FF',  # Light blue
            'service': '#A4D1FF',   # Medium light blue
            'servicetemplate': '#78B8FF',  # Medium blue
            'servicetemplategroup': '#4C9FFF',  # Darker blue
            'servicetemplategroupcomponent': '#2886FF',  # Even darker blue
            'component': '#0F6EFF',  # Dark blue
        } 
        
        # Define fields to skip (e.g., tags, problematic reverse relationships)
        excluded_fields = {
            'tags', 
            'datasource_set', 
            'custom_field_data', 
            'bookmarks', 
            'tenant', 
            'journal_entries', 
            'subscriptions'
        }

        def sanitize_label(text):
            """Sanitize a text string to be used in a Mermaid node."""
            return re.sub(r'[^a-zA-Z0-9_]', '_', text)
        
        def add_node(obj, parent_label=None, current_depth=0):
            label = f"{sanitize_label(obj._meta.model_name)}_{obj.pk}"
            
            # Prevent circular reference by ensuring we don't revisit a node
            if label in visited or current_depth > max_depth:
                return
            visited.add(label)

            # Get the color for the current object type
            obj_type = obj._meta.model_name.lower()
            color = color_map.get(obj_type, '#FFFFFF')  # Default to white if not found

            # Sanitize the object name for use in the diagram
            display_name = str(obj).replace('"', "'")  # Replace quotes to avoid breaking Mermaid syntax
            shape = f'{label}([{display_name}]):::color_{obj_type}'
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

            # Process reverse relationships (auto-created relationships)
            for rel in obj._meta.get_fields():
                if rel.is_relation and rel.auto_created and not rel.concrete and rel.name not in excluded_fields:
                    if current_depth + 1 > max_depth:
                        continue
                    # Handle GenericForeignKey relationships
                    if isinstance(rel, GenericForeignKey):
                        related_obj = getattr(obj, rel.name, None)
                        if related_obj:
                            related_label = f"{sanitize_label(related_obj._meta.model_name)}_{related_obj.pk}"
                            if (related_label, label) not in processed_relationships:
                                add_node(related_obj, label, current_depth + 1)
                    else:            
                        related_objects = getattr(obj, rel.get_accessor_name(), None)
                        if related_objects is not None and hasattr(related_objects, 'all'):
                            for related_obj in related_objects.all():
                                related_label = f"{sanitize_label(related_obj._meta.model_name)}_{related_obj.pk}"
                                if (related_label, label) not in processed_relationships:
                                    add_node(related_obj, label, current_depth + 1)
                
            # Handle the specific relationship from Component to Service to avoid circular reference loop
            if isinstance(obj, Component):
                if obj.service:
                    service = obj.service
                    service_label = f"{sanitize_label(service._meta.model_name)}_{service.pk}"
                
                    # Add the explicit link from Component to Service
                    if (label, service_label) not in processed_relationships and (service_label, label) not in processed_relationships:
                        diagram += f"{label} --> {service_label}\n"
                        processed_relationships.add((label, service_label))
                        
                # Add the explicit link from Component to ServiceTemplateComponentGroup
                if obj.template_component:
                    stgc = obj.template_component
                    stgc_label = f"{sanitize_label(stgc._meta.model_name)}_{stgc.pk}"
                
                    # Add the explicit link from Component to Service
                    if (label, stgc_label) not in processed_relationships and (stgc_label, label) not in processed_relationships:
                        diagram += f"{stgc_label} --> {label}\n"
                        processed_relationships.add((label, stgc_label))
                                
        # Start the diagram with the main object
        add_node(instance)

        legend = ''

        # Add the legend subgraph with a specific color and style
        legend += "graph LR\n"
        legend += "subgraph Legend [Legend]\n"
        legend += "direction LR\n"  # Place items in the legend in a horizontal row
       
        # Style the subgraph for the legend
        for obj_type, color in color_map.items():
            verbose_name = obj_type.replace('_', ' ').title()
            legend += f'color_{obj_type}["{verbose_name}"]:::color_{obj_type}\n'
        legend += "end\n"
        legend += "style Legend fill:#E5F2FF,stroke:#0F6EFF,stroke-width:1px;\n"
        # Append classDef styles directly to the diagram string
        for obj_type, color in color_map.items():
            legend += f'classDef color_{obj_type} fill:{color},stroke:#000,stroke-width:2px,font-weight:bold;\n'

        return legend + diagram
    
