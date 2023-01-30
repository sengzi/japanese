# Generated by Django 3.2.9 on 2022-05-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0009_novel_novel_chapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('artist', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('meaning', models.TextField()),
            ],
        ),
    ]
