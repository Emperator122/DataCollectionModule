# Generated by Django 3.1.7 on 2021-03-07 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainPage', '0002_auto_20210306_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='UchredLaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameUchred', models.CharField(blank=True, max_length=100)),
                ('fullnameUchred', models.CharField(blank=True, max_length=100)),
                ('addressUchred', models.CharField(blank=True, max_length=100)),
                ('telUchred', models.CharField(blank=True, max_length=100)),
                ('mailUchred', models.CharField(blank=True, max_length=100)),
                ('websiteUchred', models.CharField(blank=True, max_length=100)),
                ('isIndividual', models.BooleanField()),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RepInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameRep', models.CharField(blank=True, max_length=101)),
                ('addressRep', models.CharField(blank=True, max_length=100)),
                ('workTimeRep', models.CharField(blank=True, max_length=100)),
                ('telephoneRep', models.CharField(blank=True, max_length=100)),
                ('emailRep', models.CharField(blank=True, max_length=100)),
                ('websiteRep', models.CharField(blank=True, max_length=100)),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FilInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameFil', models.CharField(blank=True, max_length=100)),
                ('addressFil', models.CharField(blank=True, max_length=100)),
                ('workTimeFil', models.CharField(blank=True, max_length=100)),
                ('telephoneFil', models.CharField(blank=True, max_length=100)),
                ('emailFil', models.CharField(blank=True, max_length=100)),
                ('websiteFil', models.CharField(blank=True, max_length=100)),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Common',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('regDate', models.DateField(blank=True)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('workTime', models.CharField(blank=True, max_length=100)),
                ('telephone', models.CharField(blank=True, max_length=100)),
                ('fax', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('additionalInformation', models.CharField(blank=True, max_length=100)),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
