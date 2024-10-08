"""Top-level package for NetBox Service Management Plugin."""

__author__ = """Eric Hester"""
__email__ = "hester1@clemson.edu"
__version__ = "0.0.2"


from netbox.plugins import PluginConfig


class ServiceManagementConfig(PluginConfig):
    name = "netbox_service_management"
    verbose_name = "NetBox Service Management Plugin"
    description = "NetBox plugin for Service Management."
    version = "0.0.2"
    base_url = "netbox_service_management"


config = ServiceManagementConfig
