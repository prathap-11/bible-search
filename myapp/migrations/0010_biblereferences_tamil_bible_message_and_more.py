# Generated by Django 5.1.4 on 2024-12-19 07:55

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_author_remove_taxonomybiblestudy_add_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='biblereferences',
            name='tamil_bible_message',
            field=ckeditor.fields.RichTextField(default='valid Python', null=True),
        ),
        migrations.AlterField(
            model_name='biblereferences',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bible_references', to='myapp.author'),
        ),
    ]
