from rest_framework import routers, path
from . import views

router = routers.DefaultRouter()
router.register(r'solutions', views.SolutionViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'service_templates', views.ServiceTemplateViewSet)
router.register(r'service_template_groups', views.ServiceTemplateGroupViewSet)
router.register(r'service_template_group_components', views.ServiceTemplateGroupComponentViewSet)  
router.register(r'components', views.ComponentViewSet)
path('objects/<int:content_type_id>/', views.dynamic_object_list, name='dynamic_object_list'),

urlpatterns = router.urls