from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

plugin_buttons = [
    PluginMenuButton(
        link="plugins:netbox_service_management:service_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

items = (
    PluginMenuItem(
        link="plugins:netbox_service_management:service_list",
        link_text="Services",
        buttons=plugin_buttons,
    ),
)

menu = PluginMenu(
    label="Service Management",
    groups=(("SERVICE MANAGMENT", items),),
    icon_class="mdi mdi-group",
)

