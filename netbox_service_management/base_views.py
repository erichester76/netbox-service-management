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


        # Extract fields and their values for the object, including relationships
        field_data = []
        for field in instance._meta.get_fields():            
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
        mermaid_diagram, mermaid_legend = self.generate_mermaid_diagram(instance, max_depth=15)

        return {
            'object_name': object_name,
            'field_data': field_data,
            'related_tables': related_tables,
            'mermaid_diagram': mermaid_diagram,
            'mermaid_legend': mermaid_legend,
        }

    def generate_mermaid_diagram(self, instance, max_depth=10):
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
            'device_role',
            'role',
            'device',
            'taggeditem',
            'platform',
            'taggeditem',
            'contenttype',
            'cable',
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
            'vrf',
            'prefix'
            'clusterrole',  
        }
        
        excluded_fields = {
            'id', 
            'custom_fielddata', 
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
            'device',
            'role',
            'ipaddress'
            'depends_on',
            'dependencies',
            'created',
            'last_updated',
            'objectid',
            'primary_ip4',
            'primary_ip6',
            'ipaddresses',
            'cluster_group',
            'cluster_type',
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
                app_label = sanitize_label(obj._meta.app_label.lower())
                label = ""
                obj_type = ""
                nonlocal diagram
                

                # Skip excluded modules we dont want to show in diagram
                if parent_label and ((sanitize_label(obj._meta.model_name.lower()) in excluded_model_names)):
                    #diagram += f"%% RETURN-EXCLUDED {parent_label} depth {current_depth}\n"
                    return
               
                # Prepend label with proper netbox app label (dcim,ipam,virtualization if its not our object)
                if 'netbox_service_management' not in app_label:
                    label = f"{app_label}_{sanitize_label(obj._meta.model_name.lower())}_{obj.pk}"
                    obj_type = f"{app_label}_{obj._meta.model_name.lower()}"
                else:
                    label = f"{sanitize_label(obj._meta.model_name.lower())}_{obj.pk}"
                    obj_type = obj._meta.model_name.lower()

                # Defined as hard edges, probably need to remove backwards references on these.
                if parent_label and (current_depth > max_depth or 'cluster' in parent_label or 'servicetemplategroupcomponent' in parent_label):
                    #diagram += f"%% RETURN - EDGE PARENT {parent_label} CHILD {label} depth {current_depth}\n"
                    return

                #diagram += f"%% IN ADDNODE {parent_label} {label} {str(obj)} {current_depth}\n"

                # #define edges - I tried not to have to do it.. but I give up
                # if (label and parent_label) and ('device' in parent_label or 'cluster' in parent_label) and ('virtualmachine' in label):
                #     diagram += f"%% ETURN-vm-loop PARENT {parent_label} CHILD {label} depth {current_depth}\n"
                #     retur
                
                # if (label and parent_label) and ('servicetemplategroup' in parent_label or 'service' in parent_label) and 'servicetemplate' in label):
                #     diagram += f"%% RETURN-STG-LOOP PARENT {parent_label} CHILD {label} depth {current_depth}\n"
                #     return
                # if (label and parent_label) and 'component' in parent_label and ('service' in label and not 'ipam_service' in label):
                #     diagram += f"%% RETURN-COMP-LOOP PARENT {parent_label} CHILD:{label} depth {current_depth}\n"
                #     return
                
                # #stop at stgc in recursion so services dont wrap around
                # if parent_label and ('servicetemplategroupcomponent' in parent_label):
                #     diagram += f"%% RETURN-STGC PARENT {parent_label} CHILD {label} depth {current_depth}\n"
                #     return
                
                if parent_label and ('cluster' not in parent_label): visited.add(label)

                # Create subgraphs for service_templates
                if parent_label and (isinstance(obj, ServiceTemplate) and label+"_stgrp" not in open_subgraphs):
                    # Start a subgraph for the service template
                    add_subgraph_start(label+"_stgrp", f"T: {sanitize_display_name(str(obj))}")
                    open_subgraphs.add(label+"_stgrp")

                # Create subgraphs for services under a service_template
                if parent_label and 'solution' not in parent_label and (isinstance(obj, Service) and label+"_servgrp" not in open_subgraphs):
                    #if service_template_label in open_subgraphs:
                    # Start a subgraph for the service under the service template's subgraph
                    add_subgraph_start(label+"_servgrp", f"S: {sanitize_display_name(str(obj))}")
                    open_subgraphs.add(label+"_servgrg")

                # Sanitize the display name for the diagram
                display_name = sanitize_display_name(str(obj))
                shape = f'{label}("{display_name}"):::color_{obj_type}'
               
                #close the service subgroup before we add the item if its a cluster, we dont want it in any specific service
                if 'cluster' in label:
                    for item in list(open_subgraphs):
                        if '_servgrp' in item:
                             open_subgraphs.remove(item)
                             
                # Add the node and its clickable link if available
                add_to_diagram(shape, label, obj)

                # Add an edge from the parent node if applicable
                add_edge(parent_label, label)

                # Process relationships before marking this object as visited
                process_relationships(obj, label, current_depth)

                # Close subgraphs if they were opened
                if isinstance(obj, Service) and label+"_servgrp" in open_subgraphs:
                    add_subgraph_end(label+"_servgrp")
                    open_subgraphs.remove(label+"_servrp")

                if isinstance(obj, ServiceTemplate) and label+"_stgrp" in open_subgraphs:
                    add_subgraph_end(label+"_stgrp")
                    open_subgraphs.remove(label+"_stgrp")
                    
                



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
            diagram += f"style {label} fill:transparent,stroke-width:1px;\n"


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
            related_app_label = sanitize_label(related_obj._meta.app_label.lower())
            related_label = ""
            if 'netbox_service_management' not in related_app_label:
                related_label = f"{related_app_label}_{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}"
            else:
                related_label = f"{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}"
            nonlocal diagram
            
            if related_label not in visited or ('cluster' in related_label and 'virtualmachine' in label) or ('ServiceTemplateGroupComponent' in related_label and 'component' in label):
                #diagram += f'%% ADDNODE {related_label} calling addnode\n'
                add_node(related_obj, label, current_depth + 1)
            #else:
                #diagram += f'%% ADDNODE {related_label} in visited\n'    
                      
        def process_relationships(obj, label, current_depth):
            """
            Processes relationships for an object and recursively call add_node until we traverse the whole tree
            """
            for rel in obj._meta.get_fields():
                # Handle reverse and forward relationships, excluding certain fields.
                if rel.is_relation and (sanitize_label(obj._meta.model_name.lower()) not in excluded_model_names) and (rel.name not in excluded_fields):
                    related_objects = getattr(obj, rel.get_accessor_name(), None) if rel.auto_created else getattr(obj, rel.name, None)
                    
                    nonlocal diagram
                      
                    # Process the related objects if it's a queryset (reverse relationships)
                    if related_objects is not None and hasattr(related_objects, 'all'):
                        for related_obj in related_objects.all():
                            #diagram += f"%% FIELD {rel.name}: {sanitize_label(related_obj._meta.model_name.lower())} {sanitize_display_name(str(related_obj))}\n"
                            add_node_if_not_visited(related_obj, label, current_depth + 1)

                    # Process single related objects for forward relationships (ForeignKey, OneToOne)
                    elif related_objects: 
                        #diagram += f"%% FIELD {rel.name}: {sanitize_label(related_objects._meta.model_name.lower())} {sanitize_display_name(str(related_objects))}\n"
                        add_node_if_not_visited(related_objects, label, current_depth + 1)

            # Handle GenericForeignKey relationships like in Component
            if hasattr(obj, 'content_object') and obj.content_object:
                related_obj = obj.content_object
                add_node_if_not_visited(related_obj, label, current_depth + 1)
                add_edge(f"{sanitize_label(obj._meta.model_name.lower())}_{obj.pk}", f"{sanitize_label(related_obj._meta.app_label.lower())}_{sanitize_label(related_obj._meta.model_name.lower())}_{related_obj.pk}")


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
    