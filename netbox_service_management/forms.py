from django import forms
from django.db import models as djmodels  # Rename django.db.models to djmodels
from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from . import models

class SolutionForm(NetBoxModelForm):
    class Meta:
        model = models.Solution
        fields = ("name", "tenant", "tags")

class ServiceTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ("name", "solution", "tags")
        
class ServiceTemplateGroupForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplateGroup
        fields = ("name", "service_template", "tags")
        
class ServiceTemplateGroupComponentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplateGroupComponent
        fields = ("name", "service_template_group", "tags")
        
class ComponentForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(
            djmodels.Q(app_label='dcim') | djmodels.Q(app_label='ipam')
        ),
        label="Object Type",
        required=True,
    )
    object_id = forms.ChoiceField(label="Object", required=True)

    class Meta:
        model = models.Component
        fields = ['name', 'service', 'template_component', 'tenant', 'content_type', 'object_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically populate the object_id choices based on the selected content_type
        if 'content_type' in self.data:
            try:
                content_type = ContentType.objects.get(pk=int(self.data.get('content_type')))
                self.fields['object_id'].choices = self.get_object_choices(content_type)
            except (ValueError, ContentType.DoesNotExist):
                self.fields['object_id'].choices = []
        elif self.instance.pk and self.instance.content_type:
            content_type = self.instance.content_type
            self.fields['object_id'].choices = self.get_object_choices(content_type)
        else:
            self.fields['object_id'].choices = []

    def get_object_choices(self, content_type):
        """Return a list of tuples representing the objects of the selected content type."""
        model_class = content_type.model_class()
        return [(obj.pk, str(obj)) for obj in model_class.objects.all()]
    
class ServiceForm(NetBoxModelForm):
    class Meta:
        model = models.Service
        fields = ("name", "service_template", "deployment", "capability_category", "tenant", "tags")