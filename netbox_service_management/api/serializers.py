from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant
from .. import models

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Solution
        fields = ['id', 'name', 'tenant', 'created', 'last_updated']

class ServiceTemplateSerializer(serializers.ModelSerializer):
    solution = serializers.PrimaryKeyRelatedField(queryset=models.Solution.objects.all())

    class Meta:
        model = models.ServiceTemplate
        fields = ['id', 'name', 'solution', 'tags', 'created', 'last_updated']

class ServiceTemplateGroupSerializer(serializers.ModelSerializer):
    service_template = serializers.PrimaryKeyRelatedField(queryset=models.ServiceTemplate.objects.all())
    depends_on = serializers.PrimaryKeyRelatedField(queryset=models.ServiceTemplateGroup.objects.all(), allow_null=True)

    class Meta:
        model = models.ServiceTemplateGroup
        fields = ['id', 'name', 'service_template', 'depends_on', 'created', 'last_updated']

class ServiceTemplateGroupComponentSerializer(serializers.ModelSerializer):
    service_template_group = serializers.PrimaryKeyRelatedField(queryset=models.ServiceTemplateGroup.objects.all())

    class Meta:
        model = models.ServiceTemplateGroupComponent
        fields = ['id', 'name', 'service_template_group', 'created', 'last_updated']

class ServiceSerializer(serializers.ModelSerializer):
    service_template = serializers.PrimaryKeyRelatedField(queryset=models.ServiceTemplate.objects.all())

    class Meta:
        model = models.Service
        fields = ['id', 'name', 'service_template', 'deployment', 'tags', 'created', 'last_updated']

class ComponentSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=models.Service.objects.all())
    template_component = serializers.PrimaryKeyRelatedField(queryset=models.ServiceTemplateGroupComponent.objects.all())
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    object_id = serializers.IntegerField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = models.Component
        fields = [
            'id', 'name', 'service', 'template_component', 'content_type',
            'object_id', 'content_object', 'created', 'last_updated'
        ]

    def get_content_object(self, obj):
        """Returns the string representation of the related object."""
        if obj.content_object:
            return str(obj.content_object)
        return None
