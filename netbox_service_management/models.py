from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


class Solution(NetBoxModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:solution", args=[self.pk])

class ServiceTemplate(NetBoxModel):
    name = models.CharField(max_length=100)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='service_templates')
    
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:service_template", args=[self.pk])
    
class ServiceTemplateGroup(NetBoxModel):
    name = models.CharField(max_length=100)
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='template_groups')
    depends_on = models.ForeignKey('self', on_delete=models.CASCADE, related_name='dependencies', null=True,  blank=True)
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:service_template_component", args=[self.pk])
    
class ServiceTemplateGroupComponent(NetBoxModel):
    name = models.CharField(max_length=100)
    template_group = models.ForeignKey(ServiceTemplateGroup, on_delete=models.CASCADE, related_name='applications')
    
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_service_management:application", args=[self.pk])
    
class Service(NetBoxModel):
    name = models.CharField(max_length=100)
    service_template = models.ForeignKey(ServiceTemplate, on_delete=models.CASCADE, related_name='services')
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

class Components(NetBoxModel):
    name = models.CharField(max_length=100)
    template_component = models.ForeignKey(ServiceTemplateGroupComponent, on_delete=models.CASCADE, related_name='components')
    component_type = models.ForeignKey(
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
        return reverse("plugins:netbox_service_management:application", args=[self.pk])
    