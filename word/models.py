from distutils.command.upload import upload
from opcode import hasnargs
from django.db import models

# Create your models here.

tone_type = (
    ('五十音', '五十音'),
    ('浊音', '浊音'),
    ('半浊音', '半浊音'),
    ('拗音', '拗音'),
    ('拨音', '拨音'),
    ('促音', '促音'),
)


class Type(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Word(models.Model):
    japanese_word = models.CharField(max_length=200)
    kanji_word = models.CharField(max_length=200)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    meaning = models.CharField(max_length=200)


class Tone(models.Model):
    hiragana = models.CharField(max_length=200)
    katakana = models.CharField(max_length=200)
    romaji = models.CharField(max_length=200)
    hang = models.CharField(max_length=200)
    duan = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=tone_type, default='五十音')


class Chapter(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    basic_image = models.ImageField(upload_to='images')
    dialog_image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return f'{self.name}'


class Grammer(models.Model):
    grammer = models.TextField()
    meaning = models.TextField()
    example = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Novel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Novel_Chapter(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    meaning = models.TextField()
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'


class Song(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    artist = models.CharField(max_length=200)
    link = models.CharField(max_length=1000,default='www.youtube.com')
    content = models.TextField()
    meaning = models.TextField()
    
    def __str__(self):
        return f'{self.name}'