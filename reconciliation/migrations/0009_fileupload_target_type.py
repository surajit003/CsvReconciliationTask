# Generated by Django 5.0 on 2023-12-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reconciliation", "0008_reconciliationresults"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileupload",
            name="target_type",
            field=models.CharField(
                choices=[("Source", "Source"), ("Target", "Target")],
                default="Source",
                max_length=10,
            ),
        ),
    ]