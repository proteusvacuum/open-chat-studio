# Generated by Django 4.2 on 2023-11-02 12:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("experiments", "0050_bootstrap_voice_providers"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="experiment",
            name="llm_provider",
        ),
        migrations.RenameField(
            model_name="experiment",
            old_name="llm_provider_new",
            new_name="llm_provider",
        ),
    ]
