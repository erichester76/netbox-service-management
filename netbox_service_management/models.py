from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from netbox.models import NetBoxModel
from tenancy.models import Tenant

class Solution(NetBoxModel):
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE, null=True, blank=True, related_name='netbox_service_management_solution_tenant')

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:solution", args=[self.pk])

class ServiceTemplate(NetBoxModel):
    name = models.CharField(max_length=100)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='service_templates')
    tags = models.ManyToManyField(
        to='extras.Tag',
        related_name='netbox_service_management_service_templates'
    )
    
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:servicetemplate", args=[self.pk])
    
class ServiceTemplateGroup(NetBoxModel):
    name = models.CharField(max_length=100)
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='template_groups')
    depends_on = models.ForeignKey('self', on_delete=models.CASCADE, related_name='dependencies', null=True,  blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:servicetemplategroup", args=[self.pk])
    
class ServiceTemplateGroupComponent(NetBoxModel):
    name = models.CharField(max_length=100)
    service_template_group = models.ForeignKey(ServiceTemplateGroup, on_delete=models.CASCADE, related_name='stg_components')

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:servicetemplategroupcomponent", args=[self.pk])
    
class Service(NetBoxModel):
    DEPLOY_CHOICES = [
        ('development', 'Development'),
        ('testing', 'Testing'),
        ('functional', 'Functional'),
        ('qa', 'Functional'),
        ('production', 'Production'),
    ]
    CAPABILITY_CHOICES = [
        ('primary_mission_essential', 'Primary Mission Critical'),
        ('essential_support', 'Essential Support'),
        ('mission_resumption', 'Mission Resumption'),
        ('business_critical', 'Business Critical'),
        ('deferrable', 'Deferrable')    
    ]
    
    name = models.CharField(max_length=100)
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='services')
    deployment = models.CharField(max_length=100, choices=DEPLOY_CHOICES, default='development')
    capability_category = models.CharField(max_length=100, choices=CAPABILITY_CHOICES, default='deferrable')
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,null=True, blank=True, related_name='netbox_service_management_service_tenant')
 
    tags = models.ManyToManyField(
        to='extras.Tag',
        related_name='netbox_service_management_services'  
        # Custom related_name to avoid conflict with ipam->services
    )
    
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:service", args=[self.pk])

class Component(NetBoxModel):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='components')
    template_component = models.ForeignKey(ServiceTemplateGroupComponent, on_delete=models.CASCADE, related_name='components')
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,null=True, blank=True, related_name='netbox_service_management_component_tenant')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label='dcim') | models.Q(app_label='ipam')  # Optional: Limit to specific apps
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:component", args=[self.pk])
    