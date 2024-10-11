import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn

from . import models


class SolutionTable(NetBoxTable):
    name = tables.Column(linkify=True)
    tenant = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Solution
        fields = ("pk", "id", "name", "tenant", "actions")
        default_columns = ("name", "tenant")

class ServiceTemplateTable(NetBoxTable):
    services = tables.Column(
        accessor='get_services_list',
        verbose_name='Services',
        orderable=False
    )
    name = tables.Column(linkify=True)
    solution = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplate
        fields = ("pk", "id", "name", "solution", "services", "actions")
        default_columns = ("name", "services")

class ServiceTemplateGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_template = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplateGroup
        fields = ("pk", "id", "name", "service_template", "actions")
        default_columns = ("name", "service_template")
        
class ServiceTemplateGroupComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    service_template_group = tables.Column(linkify=True)
    table_actions = ('bulk_edit', 'bulk_delete')

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplateGroupComponent
        fields = ("pk", "id", "name", "service_template_group", "actions")
        default_columns = ("name", "service_template_group")
        
class ServiceTable(NetBoxTable):
    name = tables.Column(linkify=True)
    solution = tables.Column(linkify=True)
    tenant = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Service
        fields = ("pk", "id", "name", "solution", "tenant", "deployment", "capability_category", "actions")
        default_columns = ("name", "deployment", "capability_category", "tenant")
        
class ComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    content_object = tables.Column(linkify=True)
    service = tables.Column(linkify=True)
    tenant = tables.Column(linkify=True)
    template_component = tables.Column(linkify=True)
                         
    class Meta(NetBoxTable.Meta):
        model = models.Component
        fields = ("pk", "id", "name", "service", "template_component", "content_object", "tenant", "actions")
        default_columns = ("name", "service", "template_component")

