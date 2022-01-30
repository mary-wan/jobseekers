# Generated by Django 3.2.9 on 2022-01-30 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seekapp', '0002_auto_20220130_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=144, null=True)),
                ('last_name', models.CharField(blank=True, max_length=144, null=True)),
                ('contact', models.CharField(blank=True, max_length=10, null=True, unique=True)),
            ],
        ),
    ]
