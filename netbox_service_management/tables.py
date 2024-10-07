import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn

from . import models


class SolutionTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Solution
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)

class ServiceTemplateTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplate
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)

class ServiceTemplateGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplateGroup
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)
        
class ServiceTemplateGroupComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.ServiceTemplateGroupComponent
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)
        
class ServiceTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Service
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)
        
class ComponentTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.Component
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)

