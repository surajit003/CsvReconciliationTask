# Generated by Django 5.0 on 2023-12-15 04:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reconciliation", "0002_fileupload_errors_fileupload_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourcedata",
            name="file_upload_id",
            field=models.ForeignKey(
                default=10,
                on_delete=django.db.models.deletion.CASCADE,
                to="reconciliation.fileupload",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="targetdata",
            name="file_upload_id",
            field=models.ForeignKey(
                default=10,
                on_delete=django.db.models.deletion.CASCADE,
                to="reconciliation.fileupload",
            ),
            preserve_default=False,
        ),
    ]