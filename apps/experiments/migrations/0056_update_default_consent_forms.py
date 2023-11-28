# Generated by Django 4.2.7 on 2023-11-28 11:59

from django.db import migrations

def add_conversational_consent_text(apps, schema):
    CosentForm = apps.get_model("experiments", "ConsentForm")
    text = "Use any of the following to accept: {yes,accept,I accept}"
    CosentForm.objects.filter(is_default=True).update(conversational_consent=text)


class Migration(migrations.Migration):
    dependencies = [
        ("experiments", "0055_consentform_conversational_consent"),
    ]

    operations = [migrations.RunPython(add_conversational_consent_text, migrations.RunPython.noop)]
