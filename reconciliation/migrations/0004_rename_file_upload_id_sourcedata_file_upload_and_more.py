# Generated by Django 5.0 on 2023-12-15 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reconciliation", "0003_sourcedata_file_upload_id_targetdata_file_upload_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sourcedata",
            old_name="file_upload_id",
            new_name="file_upload",
        ),
        migrations.RenameField(
            model_name="targetdata",
            old_name="file_upload_id",
            new_name="file_upload",
        ),
    ]