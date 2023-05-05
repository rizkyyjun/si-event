# Generated by Django 4.1.5 on 2023-05-05 03:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pegawai', '__first__'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('expense', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('sk_file', models.BinaryField(null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='EventEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('honor', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('pph', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('netto', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('role', models.CharField(max_length=100, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pegawai.pegawai')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
    ]
