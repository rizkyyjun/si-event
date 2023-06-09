# Generated by Django 4.1.5 on 2023-05-05 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('employee_no', models.CharField(max_length=18)),
                ('employee_name', models.CharField(max_length=50)),
                ('employee_category', models.CharField(choices=[('S', 'Staff'), ('L', 'Lecturer')], default='S', max_length=50)),
                ('job_status', models.CharField(choices=[('D', 'Dosen'), ('A', 'Administrasi'), ('FT', 'Fungsional Tertentu')], default='A', max_length=50)),
                ('grade_level', models.CharField(default='-', max_length=10)),
                ('employment_status', models.CharField(max_length=50)),
                ('nama_di_rekening', models.CharField(max_length=50)),
                ('nama_bank', models.CharField(max_length=50)),
                ('nomor_rekening', models.CharField(max_length=50)),
                ('nomor_npwp', models.CharField(max_length=20)),
                ('alamat_npwp', models.CharField(max_length=200)),
                ('tombstone', models.BooleanField(default=False)),
            ],
        ),
    ]
