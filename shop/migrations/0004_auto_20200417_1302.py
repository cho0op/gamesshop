# Generated by Django 3.0.4 on 2020-04-17 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='name',
            new_name='title',
        ),
    ]