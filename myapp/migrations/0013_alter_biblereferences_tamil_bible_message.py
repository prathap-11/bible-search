# Generated by Django 5.1.4 on 2024-12-19 09:37

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_biblereferences_bookname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biblereferences',
            name='tamil_bible_message',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
