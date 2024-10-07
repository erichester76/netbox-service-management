from netbox.filtersets import NetBoxModelFilterSet
from .models import Service


# class ServiceFilterSet(NetBoxModelFilterSet):
#
#     class Meta:
#         model = Service
#         fields = ['name', ]
#
#     def search(self, queryset, name, value):
#         return queryset.filter(description__icontains=value)
