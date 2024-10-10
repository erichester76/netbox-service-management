from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu


items = (
        PluginMenuItem(
        link="plugins:netbox_service_management:solution_list",
        link_text="Solutions",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_management:solution_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_management:solution_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
        PluginMenuItem(
        link="plugins:netbox_service_management:servicetemplate_list",
        link_text="Service Templates",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_management:servicetemplate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_management:servicetemplate_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
        PluginMenuItem(
        link="plugins:netbox_service_management:servicetemplategroup_list",
        link_text="Service Template Groups",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_management:servicetemplategroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_management:servicetemplategroup_import",
                title="Import",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.BLUE,
            ),
        ]
    ),
    PluginMenuItem(
        link="plugins:netbox_service_management:servicetemplategroupcomponent_list",
        link_text="Service Template Components",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_management:servicetemplategroupcomponent_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_management:servicetemplategroupcomponent_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),   
    PluginMenuItem(
        link="plugins:netbox_service_management:service_list",
        link_text="Service",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_management:service_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_management:service_import",
                title="Import",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.BLUE,
            ),
        ]
    ),
       PluginMenuItem(
        link="plugins:netbox_service_management:component_list",
        link_text="Service Components",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_service_management:component_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_service_management:component_import",
                title="Import",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.BLUE,
            ),
        ]
    ),
    
)

menu = PluginMenu(
    label="Service Management",
    groups=(("SERVICE MANAGMENT", items),),
    icon_class="mdi mdi-group",
)

