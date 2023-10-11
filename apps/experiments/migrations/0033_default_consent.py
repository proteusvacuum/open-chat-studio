# Generated by Django 4.2 on 2023-09-28 07:13
from django.db import migrations, models
import django.db.models.deletion

DEFAULT_CONSENT_TEXT = """
Welcome to this chatbot built on Open Chat Studio! 

The Chatbot is provided "as-is" and "as available." Open Chat Studio makes no warranties,
express or implied, regarding the Chatbot's accuracy, completeness, or availability.

You use the chatbot at your own risk. Open Chat Studio shall not be liable for any harm
or damages that may result from your use of the chatbot.

You understand and agree that any reliance on the Chatbot's responses is solely at your own
discretion and risk.

By selecting “I Agree” below, you indicate that: 

* You have read and understood the above information.
* You voluntarily agree to try out this chatbot.
* You are 18 years or older.
"""


def create_default_consent(apps, schema_editor):
    ConsentForm = apps.get_model("experiments", "ConsentForm")
    if not ConsentForm.objects.filter(is_default=True).exists():
        ConsentForm.objects.create(
            name="Default Consent",
            consent_text=DEFAULT_CONSENT_TEXT,
            is_default=True
        )


def populate_experiments_consent(apps, schema_editor):
    ConsentForm = apps.get_model("experiments", "ConsentForm")
    Experiment = apps.get_model("experiments", "Experiment")
    default_consent = ConsentForm.objects.get(is_default=True)
    Experiment.objects.filter(consent_form__isnull=True).update(consent_form=default_consent)


class Migration(migrations.Migration):
    dependencies = [
        ("experiments", "0032_load_synthetic_voices"),
    ]

    operations = [
        migrations.AddField(
            model_name="consentform",
            name="is_default",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(create_default_consent, migrations.RunPython.noop),
        migrations.RunPython(populate_experiments_consent, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="experiment",
            name="consent_form",
            field=models.ForeignKey(
                help_text="Consent form content to show to users before participation in experiments.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experiments",
                to="experiments.consentform",
            ),
        ),
    ]
