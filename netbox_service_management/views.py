from netbox.views import generic
from .base_views import BaseDetailView  # Import the base class

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

class SolutionDetailView(BaseDetailView):
    queryset = Solution.objects.prefetch_related('tags')
    table = tables.SolutionTable
    
class SolutionListView(generic.ObjectListView):
    queryset = Solution.objects.prefetch_related('tags')
    table = tables.SolutionTable

class SolutionEditView(generic.ObjectEditView):
    queryset = Solution.objects.prefetch_related('tags')
    form = forms.SolutionForm

class SolutionDeleteView(generic.ObjectDeleteView):
    queryset = Solution.objects.prefetch_related('tags')
    
class ServiceTemplateDetailView(BaseDetailView):
    queryset = ServiceTemplate.objects.prefetch_related('tags')

class ServiceTemplateListView(generic.ObjectListView):
    queryset = ServiceTemplate.objects.prefetch_related('tags')
    table = tables.ServiceTemplateTable

class ServiceTemplateEditView(generic.ObjectEditView):
    queryset = ServiceTemplate.objects.prefetch_related('tags')
    form = forms.ServiceTemplateForm

class ServiceTemplateDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplate.objects.prefetch_related('tags')

class ServiceTemplateGroupDetailView(BaseDetailView):
    queryset = ServiceTemplateGroup.objects.prefetch_related('tags')

class ServiceTemplateGroupListView(generic.ObjectListView):
    queryset = ServiceTemplateGroup.objects.prefetch_related('tags')
    table = tables.ServiceTemplateGroupTable

class ServiceTemplateGroupEditView(generic.ObjectEditView):
    queryset = ServiceTemplateGroup.objects.prefetch_related('tags')
    form = forms.ServiceTemplateGroupForm

class ServiceTemplateGroupDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplateGroup.objects.prefetch_related('tags')

class ServiceTemplateGroupComponentDetailView(BaseDetailView):
    queryset = ServiceTemplateGroupComponent.objects.prefetch_related('tags')

class ServiceTemplateGroupComponentListView(generic.ObjectListView):
    queryset = ServiceTemplateGroupComponent.objects.prefetch_related('tags')
    table = tables.ServiceTemplateGroupComponentTable

class ServiceTemplateGroupComponentEditView(generic.ObjectEditView):
    queryset = ServiceTemplateGroupComponent.objects.prefetch_related('tags')
    form = forms.ServiceTemplateGroupComponentForm

class ServiceTemplateGroupComponentDeleteView(generic.ObjectDeleteView):
    queryset = ServiceTemplateGroupComponent.objects.prefetch_related('tags')

class ServiceDetailView(BaseDetailView):
    queryset = Service.objects.prefetch_related('tags')

class ServiceListView(generic.ObjectListView):
    queryset = Service.objects.prefetch_related('tags')
    table = tables.ServiceTable

class ServiceEditView(generic.ObjectEditView):
    queryset = Service.objects.prefetch_related('tags')
    form = forms.ServiceForm

class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = Service.objects.prefetch_related('tags')

class ComponentDetailView(BaseDetailView):
    queryset = Component.objects.prefetch_related('tags')

class ComponentListView(generic.ObjectListView):
    queryset = Component.objects.prefetch_related('tags')
    table = tables.ComponentTable

class ComponentEditView(generic.ObjectEditView):
    queryset = Component.objects.prefetch_related('tags')
    form = forms.ComponentForm

class ComponentDeleteView(generic.ObjectDeleteView):
    queryset = Component.objects.prefetch_related('tags')

