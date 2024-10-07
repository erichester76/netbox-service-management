import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn

from . import models


class SolutionTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Solution
        fields = ("pk", "id", "name", "tenant", "actions")
        default_columns = ("name", "tenant")

class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplate
        fields = ("pk", "id", "name", "solution", "actions")
        default_columns = ("name","solution")

class ServiceTemplateGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplateGroup
        fields = ("pk", "id", "name", "service_template" "actions")
        default_columns = ("name", "service_template")
        
class ServiceTemplateGroupComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplateGroupComponent
        fields = ("pk", "id", "name", "service_template_group" "actions")
        default_columns = ("name","service_template_group")
        
class ServiceTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Service
        fields = ("pk", "id", "name", "solution", "deployment", "actions")
        default_columns = ("name", "solution", "deployment")
        
class ComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Component
        fields = ("pk", "id", "name", "service", "template_component", "actions")
        default_columns = ("name", "service", "template_component")

