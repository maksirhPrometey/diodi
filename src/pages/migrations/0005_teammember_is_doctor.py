from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_homepage_benefits_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='is_doctor',
            field=models.BooleanField(
                default=False,
                help_text='Показувати блок «Записатись до лікаря» на сторінці профілю.',
                verbose_name='Лікар',
            ),
        ),
    ]
