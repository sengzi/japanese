# Generated by Django 3.2.9 on 2021-11-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_word_meaning'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hiragana', models.CharField(max_length=200)),
                ('katakana', models.CharField(max_length=200)),
                ('romaji', models.CharField(max_length=200)),
            ],
        ),
    ]
