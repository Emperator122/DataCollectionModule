# Generated by Django 3.1.7 on 2021-03-14 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPage', '0007_auto_20210314_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uchredlaw',
            name='isIndividual',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
