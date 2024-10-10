from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views


urlpatterns = (
    path("solutions/", views.SolutionListView.as_view(), name="solution_list"),
    path("solutions/add/", views.SolutionEditView.as_view(), name="solution_add"),
    path("solutions/<int:pk>/", views.SolutionDetailView.as_view(), name="solution"),
    path("solutions/<int:pk>/edit/", views.SolutionEditView.as_view(), name="solution_edit"),
    path("solutions/<int:pk>/delete/", views.SolutionDeleteView.as_view(), name="solution_delete"),
    path("solutions/<int:pk>/changelog/", views.SolutionChangeLogView.as_view(),name="solution_changelog"),
    
    path("service_templates/", views.ServiceTemplateListView.as_view(), name="servicetemplate_list"),
    path("service_templates/add/", views.ServiceTemplateEditView.as_view(), name="servicetemplate_add"),
    path("service_templates/<int:pk>/", views.ServiceTemplateDetailView.as_view(), name="servicetemplate"),
    path("service_templates/<int:pk>/edit/", views.ServiceTemplateEditView.as_view(), name="servicetemplate_edit"),
    path("service_templates/<int:pk>/delete/", views.ServiceTemplateDeleteView.as_view(), name="servicetemplate_delete"),
    path("service_templates/<int:pk>/changelog/", views.ServiceTemplateChangeLogView.as_view(),name="servicetemplate_changelog"),
    
    path("service_template_groups/", views.ServiceTemplateGroupListView.as_view(), name="servicetemplategroup_list"),
    path("service_template_groups/add/", views.ServiceTemplateGroupEditView.as_view(), name="servicetemplategroup_add"),
    path("service_template_groups/<int:pk>/", views.ServiceTemplateGroupDetailView.as_view(), name="servicetemplategroup"),
    path("service_template_groups/<int:pk>/edit/", views.ServiceTemplateGroupEditView.as_view(), name="servicetemplategroup_edit"),
    path("service_template_groups/<int:pk>/delete/", views.ServiceTemplateGroupDeleteView.as_view(), name="servicetemplategroup_delete"),
    path("service_template_groups/<int:pk>/changelog/", views.ServiceTemplateGroupChangeLogView.as_view(), name="servicetemplategroup_changelog"),
    
    path("service_template_group_components/", views.ServiceTemplateGroupComponentListView.as_view(), name="servicetemplategroupcomponent_list"),
    path("service_template_group_components/add/", views.ServiceTemplateGroupComponentEditView.as_view(), name="servicetemplategroupcomponent_add"),
    path("service_template_group_components/<int:pk>/", views.ServiceTemplateGroupComponentDetailView.as_view(), name="servicetemplategroupcomponent"),
    path("service_template_groups/<int:pk>/edit/", views.ServiceTemplateGroupComponentEditView.as_view(), name="servicetemplategroupcomponent_edit"),
    path("service_template_groups/<int:pk>/delete/", views.ServiceTemplateGroupComponentDeleteView.as_view(), name="servicetemplategroupcomponent_delete"),
    path("service_template_groups/<int:pk>/changelog/", views.ServiceTemplateGroupComponentChangeLogView.as_view(), name="servicetemplategroupcomponent_changelog", kwargs={"model": models.Solution},
),
    
    path("components/", views.ComponentListView.as_view(), name="component_list"),
    path("components/add/", views.ComponentEditView.as_view(), name="component_add"),
    path("components/<int:pk>/", views.ComponentDetailView.as_view(), name="component"),
    path("components/<int:pk>/edit/", views.ComponentEditView.as_view(), name="component_edit"),
    path("components/<int:pk>/delete/", views.ComponentDeleteView.as_view(), name="component_delete"),
    path("components/<int:pk>/changelog/", views.ComponentChangeLogView.as_view(), name="component_changelog"), 
    
    path("services/", views.ServiceListView.as_view(), name="service_list"),
    path("services/add/", views.ServiceEditView.as_view(), name="service_add"),
    path("services/<int:pk>/", views.ServiceDetailView.as_view(), name="service"),
    path("services/<int:pk>/edit/", views.ServiceEditView.as_view(), name="service_edit"),
    path("services/<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="service_delete"),
    path("services/<int:pk>/changelog/", views.ServiceChangeLogView.as_view(), name="service_changelog"),
    
    #Bulk Imports
    path('solutions/import/', views.SolutionImportView.as_view(), name='solution_import'),
    path('services/import/', views.ServiceImportView.as_view(), name='service_import'),
    path('service-templates/import/', views.ServiceTemplateImportView.as_view(), name='servicetemplate_import'),
    path('service-template-groups/import/', views.ServiceTemplateGroupImportView.as_view(), name='servicetemplategroup_import'),
    path('service-template-group-components/import/', views.ServiceTemplateGroupComponentImportView.as_view(), name='servicetemplategroupcomponent_import'),
    path('components/import/', views.ComponentImportView.as_view(), name='component_import'),

)

