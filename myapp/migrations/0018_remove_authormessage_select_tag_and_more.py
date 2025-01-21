# Generated by Django 5.1.4 on 2025-01-21 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_authormessage_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authormessage',
            name='select_tag',
        ),
        migrations.AddField(
            model_name='authormessage',
            name='select_tag',
            field=models.ManyToManyField(related_name='selected_tags', to='myapp.taxonomybiblestudy'),
        ),
    ]
