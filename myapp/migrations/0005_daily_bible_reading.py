# Generated by Django 5.1.4 on 2024-12-11 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_verse_of_the_day_alter_dailyverse_day_chapter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily_bible_reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('bookname', models.CharField(max_length=20)),
                ('tamilname', models.CharField(max_length=20)),
                ('chapter', models.IntegerField()),
            ],
        ),
    ]
