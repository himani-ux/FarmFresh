# Generated by Django 5.2 on 2025-04-11 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('category', models.IntegerField(choices=[(1, 'Fruits & Vegetables '), (2, 'Pulses & Cereals'), (3, 'Farming Tools and Equipements'), (4, 'Dairy Products'), (5, 'Herbs'), (6, 'Nursery & Plants')])),
                ('is_available', models.BooleanField(default=True)),
                ('pimage', models.ImageField(upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='AgroSeed.product')),
            ],
        ),
    ]
