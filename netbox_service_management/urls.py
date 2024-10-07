from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views


urlpatterns = (
    path("services/", views.ServiceListView.as_view(), name="service_list"),
    path("services/add/", views.ServiceEditView.as_view(), name="service_add"),
    path("services/<int:pk>/", views.ServiceDetailView.as_view(), name="service_detail"),
    path("services/<int:pk>/edit/", views.ServiceEditView.as_view(), name="service_edit"),
    path("services/<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="service_delete"),
    path(
        "services/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="service_changelog",
        kwargs={"model": models.Service},
    ),
)
