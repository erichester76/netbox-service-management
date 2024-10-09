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

from dcim.models import Device

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
            # 'service_templates',
            # 'stg_components',
            # 'components',
            # 'template_groups',
            # 'services',
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
                        model_name = related_model._meta.model_name.lower()
                        add_url = reverse(
                            f'plugins:netbox_service_management:{model_name}_add'
                        )   
                        # Pre-fill the linking field with the current object's ID, if possible
                        add_url += f'?{instance._meta.model_name.lower()}={instance.pk}'

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
        mermaid_diagram, mermaid_legend = self.generate_mermaid_diagram(instance, max_depth=20)

        return {
            'object_name': object_name,
            'field_data': field_data,
            'related_tables': related_tables,
            'mermaid_diagram': mermaid_diagram,
            'mermaid_legend': mermaid_legend,
        }

    def generate_mermaid_diagram(self, instance, max_depth=1):
        # Initialize the diagram string
        diagram = "graph TD\n"
        visited = set()
        processed_relationships = set()  # Track relationships to prevent circular references
        
         # Define colors for each model type
        color_map = {
            'solution': '#16a2b8',  # Darker Teal 
            'service': '#184990',   # Teal 
            'servicetemplate': '#02252f',  # GreenBlue
            'servicetemplategroup': '#f59f01',  # Orange1
            'servicetemplategroupcomponent': '#f76706',  # Orange2
            'component': '#d63a39',  # Red 
        }

        excluded_model_names = {
            'virtualdisk',
            'vminterface',
            'site',
            'platform',
            'ipaddress'
            'devicerole',
            'taggeditem',
            'platform',
            'taggeditem',
            'contenttype',
            'cable',
            'cluster',
            'devicetype',
            'interface',
            'manufacturer',
            'tag',
            'tenant',
            'tenantgroup',
            'topology',
            'vlan',
            'coordinate',
            'cabletermination',
            
        }

        def sanitize_label(text):
            """Sanitize a text string to be used in a Mermaid node."""
            return re.sub(r'[^a-zA-Z0-9_]', '_', text)
        
        def sanitize_display_name(name):
            """
            Sanitizes the object name for use in the diagram.
            """
            return re.sub(r'[^a-zA-Z0-9_\.\ \-\/]', '', name)
       
        open_subgraphs = set()

        def add_node(obj, parent_label=None, current_depth=0):
                """
                Recursively adds nodes to the diagram, handling relationships and avoiding circular references.
                """
                app_label = obj._meta.app_label.lower()
                label = ""
                obj_type = ""
                
                if 'netbox_service_management' not in app_label:
                    label = f"{app_label}_{sanitize_label(obj._meta.model_name.lower())}_{obj.pk}"
                    obj_type = f"{app_label}_{obj._meta.model_name.lower()}"
                else:
                    label = f"{sanitize_label(obj._meta.model_name.lower())}_{obj.pk}"
                    obj_type = obj._meta.model_name.lower()

                # Check if we've already visited this node with its relationships processed.
                if label in visited or current_depth > max_depth:
                    return

                #stop at clusters in recursion so we dont draw the whole platform
                #if parent_label and ('cluster' in parent_label):
                #    return
                
                if sanitize_label(obj._meta.model_name.lower()) in excluded_model_names:
                    return
                
                visited.add(label)

                # Handle subgraphs for service_templates
                if isinstance(obj, ServiceTemplate) and label not in open_subgraphs:
                    # Start a subgraph for the service template
                    add_subgraph_start(label+"_sg", f"T: {sanitize_display_name(str(obj))}")
                    open_subgraphs.add(label+"_sg")

                # Handle subgraphs for services under a service_template
                if isinstance(obj, Service) and label+"_sg" not in open_subgraphs:
                    service_template_label = f"{obj.service_template._meta.model_name.lower()}_{obj.service_template.pk}_sg"
                    if service_template_label in open_subgraphs:
                        # Start a subgraph for the service under the service template's subgraph
                        add_subgraph_start(label+"_sg", f"S: {sanitize_display_name(str(obj))}")
                        open_subgraphs.add(label+"_sg")

                # Sanitize the display name for the diagram
                display_name = sanitize_display_name(str(obj))
                shape = f'{label}("{display_name}"):::color_{obj_type}'

                # Add the node and its clickable link if available
                add_to_diagram(shape, label, obj)

                # Add an edge from the parent node if applicable
                add_edge(parent_label, label)

                # Process relationships before marking this object as visited
                process_relationships(obj, label, current_depth)

                # Close subgraphs if they were opened
                if isinstance(obj, Service) and label+"_sg" in open_subgraphs:
                    add_subgraph_end(label+"_sg")
                    open_subgraphs.remove(label+"_sg")

                if isinstance(obj, ServiceTemplate) and label+"_sg" in open_subgraphs:
                    add_subgraph_end(label+"_sg")
                    open_subgraphs.remove(label+"_sg")

                # Now mark the object as visited to ensure we don't reprocess it
                visited.add(label)

        def add_subgraph_start(label, description):
            """
            Adds the start of a subgraph with a given label and description.
            """
            nonlocal diagram
            diagram += f"subgraph {label} [{description}]\n"

        def add_subgraph_end(label):
            """
            Ends the most recent subgraph.
            """
            nonlocal diagram
            diagram += "end\n"
            diagram += f"style {label} fill:transparent,stroke-width:0px;\n"


        def add_to_diagram(shape, label, obj):
            """
            Adds a node shape to the diagram and includes a clickable link if applicable.
            """
            nonlocal diagram
            diagram += shape + "\n"
            if hasattr(obj, 'get_absolute_url'):
                diagram += f'click {label} "{obj.get_absolute_url()}"\n'

        def add_edge(parent_label, label):
            """
            Adds an edge between the parent and the current label, avoiding duplicates.
            """
            if parent_label and label and (parent_label, label) not in processed_relationships and (label, parent_label) not in processed_relationships:
                nonlocal diagram
                diagram += f"{parent_label} --> {label}\n"
                processed_relationships.add((parent_label, label))
          
        def add_node_if_not_visited(related_obj, label, current_depth):
            """
            Adds a related object to the diagram if it hasn't been visited.
            """
            # Include the app label to distinguish between similar model names
            related_app_label = related_obj._meta.app_label.lower()
            related_label = ""
            if 'netbox_service_management' not in related_app_label:
                related_label = f"{related_app_label}_{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}"
            else:
                related_label = f"{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}"
                
            if related_label not in visited:
                add_node(related_obj, label, current_depth + 1)
                      
        def process_relationships(obj, label, current_depth):
            """
            Processes relationships for an object and recursively call add_node until we traverse the whole tree
            """
            for rel in obj._meta.get_fields():
                # Handle reverse and forward relationships, excluding certain fields.
                if rel.is_relation and (sanitize_label(obj._meta.model_name.lower()) not in excluded_model_names):
                    related_objects = getattr(obj, rel.get_accessor_name(), None) if rel.auto_created else getattr(obj, rel.name, None)
                    
                    # Process the related objects if it's a queryset (reverse relationships)
                    if related_objects is not None and hasattr(related_objects, 'all'):
                        for related_obj in related_objects.all():
                            # Special case: if the related object is a Device with an assigned Cluster, use the Cluster instead
                            if isinstance(related_obj, Device) and related_obj.cluster:
                                cluster = getattr(related_obj, 'cluster', None)
                                if cluster:
                                    related_obj = cluster                            
                            # add the edge for the service to component now on the forward recursion
                            if (isinstance(related_obj,Component) and isinstance(obj,Service)):
                                related_label = f"{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}"
                                add_edge(label,related_label)
                            else:
                                add_node_if_not_visited(related_obj, label, current_depth + 1)

                    # Process single related objects for forward relationships (ForeignKey, OneToOne)
                    elif related_objects:
                        # Special case: if the related object is a Device with an assigned Cluster, use the Cluster instead
                        if isinstance(related_objects, Device) and related_objects.cluster:
                            cluster = getattr(related_objects, 'cluster', None)
                            if cluster:
                                related_objects = cluster                                 
                        #stop the component to service link so we can recurse back from
                        if not (isinstance(related_objects,Service) and isinstance(obj,Component)): 
                            add_node_if_not_visited(related_objects, label, current_depth + 1)

            # Handle GenericForeignKey relationships like in Component
            if hasattr(obj, 'content_object') and obj.content_object:
                related_obj = obj.content_object
                add_node_if_not_visited(related_obj, label, current_depth + 1)
                add_edge(f"{sanitize_label(obj._meta.model_name.lower())}_{obj.pk}", f"{related_obj._meta.app_label.lower()}_{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}")


        # Start the diagram with the main object
        add_node(instance)

        # Add the legend subgraph with a specific color and style
        legend = "graph LR\n"
        legend += "direction LR\n"  # Place items in the legend in a horizontal row
        legend += "subgraph Legend [Legend]\n"
        
        # Style the subgraph for the legend
        for obj_type, color in color_map.items():
            verbose_name = re.sub(r'[^a-zA-Z0-9_]', '_', obj_type)
            legend += f'key_{obj_type}({verbose_name}):::color_{obj_type}\n'
        legend += "end\n"
        legend += "style Legend fill:transparent,stroke-width:0px;\n"
        
        # Append classDef styles directly to the diagram string
        for obj_type, color in color_map.items():
            legend += f'classDef color_{obj_type} fill:{color},stroke:#000,stroke-width:0px,color:#fff,font-size:14px;\n'
            diagram += f'classDef color_{obj_type} fill:{color},stroke:#000,stroke-width:0px,color:#fff,font-size:14px;\n'
        return diagram, legend
    
