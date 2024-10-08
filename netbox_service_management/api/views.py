from rest_framework import viewsets
from .. import models
from . import serializers
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

class SolutionViewSet(viewsets.ModelViewSet):
    queryset = models.Solution.objects.all()
    serializer_class = serializers.SolutionSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class ServiceTemplateViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceTemplate.objects.all()
    serializer_class = serializers.ServiceTemplateSerializer

class ServiceTemplateGroupViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceTemplateGroup.objects.all()
    serializer_class = serializers.ServiceTemplateGroupSerializer

class ServiceTemplateGroupComponentViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceTemplateGroupComponent.objects.all()
    serializer_class = serializers.ServiceTemplateGroupComponentSerializer

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = models.Component.objects.all()
    
def dynamic_object_list(request, content_type_id):
    try:
        content_type = ContentType.objects.get(pk=content_type_id)
        model_class = content_type.model_class()
        objects = model_class.objects.all()
        data = [{'pk': obj.pk, 'name': str(obj)} for obj in objects]
        return JsonResponse(data, safe=False)
    except ContentType.DoesNotExist:
        return JsonResponse([], safe=False)