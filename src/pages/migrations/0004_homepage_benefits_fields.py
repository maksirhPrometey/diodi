from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_aboutpage_contactspage_gallery_galleryimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='benefits_title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Заголовок блоку переваг'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='benefits_lead',
            field=models.TextField(blank=True, verbose_name='Текст блоку переваг'),
        ),
    ]
