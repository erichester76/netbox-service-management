import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('netbox_service_management', '0002_added_capability'),
        ('tenancy', '0015_contactassignment_rename_content_type'),
    ]

    # operations = [
    #     migrations.AddField(
    #         model_name='component',
    #         name='tenant',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='netbox_service_management_component_tenant', to='tenancy.tenant'),
    #     ),
    #     migrations.AddField(
    #         model_name='service',
    #         name='tenant',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='netbox_service_management_service_tenant', to='tenancy.tenant'),
    #     ),
    #     migrations.AlterField(
    #         model_name='solution',
    #         name='tenant',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='netbox_service_management_solution_tenant', to='tenancy.tenant'),
    #     ),
    # ]