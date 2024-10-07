from django import forms
from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField

from . import models

class SolutionForm(NetBoxModelForm):
    class Meta:
        model = models.Solution
        fields = ("name", "tags")

class ServiceTemplateForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplate
        fields = ("name", "tags")
        
class ServiceTemplateGroupForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplateGroup
        fields = ("name", "tags")
        
class ServiceTemplateGroupComponentForm(NetBoxModelForm):
    class Meta:
        model = models.ServiceTemplateGroupComponent
        fields = ("name", "tags")
        
class ComponentForm(NetBoxModelForm):
    class Meta:
        model = models.Component
        fields = ("name", "tags")                        

class ServiceForm(NetBoxModelForm):
    class Meta:
        model = models.Service
        fields = ("name", "tags")