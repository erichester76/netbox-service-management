from rest_framework import viewsets
from .. import models
from . import serializers

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
    serializer_class = serializers.ComponentSerializer
