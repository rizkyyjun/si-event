# Generated by Django 4.1.5 on 2023-05-05 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_sso', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NonSSOAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=150)),
                ('email', models.EmailField(default='', max_length=254)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('User', 'User'), ('Staff Keuangan', 'Staff Keuangan'), ('Guest', 'Guest')], max_length=20)),
                ('is_first_login', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=150)),
                ('email', models.EmailField(default='', max_length=254)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('User', 'User'), ('Staff Keuangan', 'Staff Keuangan'), ('Guest', 'Guest')], max_length=20)),
                ('accountType', models.CharField(choices=[('Non SSO UI', 'Non SSO UI'), ('SSO UI', 'SSO UI')], default='', max_length=20)),
                ('accNonSSO', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.nonssoaccount')),
                ('accSSO', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth_sso.ssouiaccount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
