# Generated by Django 5.1.4 on 2024-12-19 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_correction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_author', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='taxonomybiblestudy',
            name='add_author',
        ),
    ]
