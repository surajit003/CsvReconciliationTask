# Generated by Django 5.0 on 2023-12-15 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reconciliation", "0012_remove_fileupload_errors_sourcetargetfilepair_errors"),
    ]

    operations = [
        migrations.AddField(
            model_name="reconciliationresults",
            name="source_target_file_pair",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="reconciliation.sourcetargetfilepair",
            ),
            preserve_default=False,
        ),
    ]
