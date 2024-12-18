# Generated by Django 5.1.4 on 2024-12-16 08:32

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_daily_bible_reading'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxonomyBibleStudy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_taxonomy', models.CharField(max_length=200)),
                ('add_author', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BibleReferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('select_book', models.CharField(max_length=100)),
                ('chapter', models.IntegerField()),
                ('tamil_bible_message', ckeditor.fields.RichTextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bible_references', to='myapp.taxonomybiblestudy')),
                ('select_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_tags', to='myapp.taxonomybiblestudy')),
            ],
        ),
    ]