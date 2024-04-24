# Generated by Django 5.0.4 on 2024-04-24 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.division')),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('female', 'female'), ('male', 'male')], max_length=30)),
                ('birth_date', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=50)),
                ('blood_group', models.CharField(choices=[('1', 'A+'), ('2', 'A-'), ('3', 'B+'), ('4', 'B-'), ('5', 'AB+'), ('6', 'AB-'), ('7', 'O+'), ('8', 'O-')], max_length=50)),
                ('image', models.ImageField(upload_to='images/user/')),
                ('last_donate', models.DateField(blank=True, null=True)),
                ('availabilities', models.BooleanField(default=True)),
                ('District', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.district')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.division')),
            ],
        ),
        migrations.CreateModel(
            name='DonationRequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('disease', models.TextField()),
                ('location', models.CharField(max_length=50)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.usermodel')),
            ],
        ),
    ]
