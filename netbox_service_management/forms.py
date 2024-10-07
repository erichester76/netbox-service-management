from django import forms
from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField

from .models import Service


class ServiceForm(NetBoxModelForm):
    class Meta:
        model = Service
        fields = ("name", "tags")
