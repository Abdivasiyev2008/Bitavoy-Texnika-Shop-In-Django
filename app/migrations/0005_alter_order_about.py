# Generated by Django 4.2.6 on 2023-11-26 09:28

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_favouriteitem_favoriteitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='about',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
