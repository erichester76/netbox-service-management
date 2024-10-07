from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu


items = (
    PluginMenuItem(
        link="plugins:netbox_service_management:solutions_list",
        link_text="Solutions",
        buttons=PluginMenuButton(
            link="plugins:netbox_service_management:solutions_add",
            title="Add",
            icon_class="mdi mdi-plus-thick",
        )   
    ),
    PluginMenuItem(
        link="plugins:netbox_service_management:service_list",
        link_text="Service Templates",
        buttons=PluginMenuButton(
            link="plugins:netbox_service_management:service_add",
            title="Add",
            icon_class="mdi mdi-plus-thick",
        )   
    ),  
    PluginMenuItem(
        link="plugins:netbox_service_management:service_list",
        link_text="Services",
        buttons=PluginMenuButton(
            link="plugins:netbox_service_management:service_add",
            title="Add",
            icon_class="mdi mdi-plus-thick",
        )   
    ),  
    PluginMenuItem(
        link="plugins:netbox_service_management:component_list",
        link_text="Components",
        buttons=PluginMenuButton(
            link="plugins:netbox_service_management:component_add",
            title="Add",
            icon_class="mdi mdi-plus-thick",
        )   
    ),
    
)

menu = PluginMenu(
    label="Service Management",
    groups=(("SERVICE MANAGMENT", items),),
    icon_class="mdi mdi-group",
)

