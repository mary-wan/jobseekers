# Generated by Django 3.2.9 on 2022-01-26 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seekapp', '0002_rename_user_portfolio_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='User',
            new_name='user',
        ),
    ]
