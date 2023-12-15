# Generated by Django 5.0 on 2023-12-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reconciliation", "0011_remove_fileupload_status_sourcetargetfilepair"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fileupload",
            name="errors",
        ),
        migrations.AddField(
            model_name="sourcetargetfilepair",
            name="errors",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
