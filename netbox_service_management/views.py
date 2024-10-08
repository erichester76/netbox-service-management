from netbox.views import generic
from . import filtersets, forms, models, tables


class SolutionDetailView(generic.ObjectView):
    queryset = models.Solution.objects.all()
    
    def get_extra_context(self, request, instance):
        # Extract fields and their values for the object
        field_data = []
        for field in instance._meta.get_fields():
            if not field.is_relation:  # Skip relationships if not needed
                value = getattr(instance, field.name, None)
                field_data.append({
                    'name': field.verbose_name if hasattr(field, 'verbose_name') else field.name,
                    'value': value,
                })

        # Get all ServiceTemplate instances related to this Solution
        service_templates = models.ServiceTemplate.objects.filter(solution=instance)
        service_templates_table = tables.ServiceTemplateTable(service_templates)
        
        # Get all Services that are linked to the above ServiceTemplates
        services = models.Service.objects.filter(service_template__in=service_templates)
        services_table = tables.ServiceTable(services)

        return {
            'field_data': field_data,
            'service_templates_table': service_templates_table,
            'services_table': services_table,
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

