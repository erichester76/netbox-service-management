"""Top-level package for NetBox Service Management Plugin."""
from importlib_metadata import version

__version__ = version(__package__)
__author__ = """Eric Hester"""
__email__ = "hester1@clemson.edu"


from netbox.plugins import PluginConfig


class ServiceManagementConfig(PluginConfig):
    name = "netbox_service_management"
    verbose_name = "NetBox Service Management Plugin"
    description = "NetBox plugin for Service Management."
    version = "__version__"
    base_url = "netbox_service_management"


config = ServiceManagementConfig
