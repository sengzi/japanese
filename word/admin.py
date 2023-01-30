from django.contrib import admin
from .models import Type, Word, Tone, Chapter, Grammer, Novel, Novel_Chapter, Song
# Register your models here.


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class WordAdmin(admin.ModelAdmin):
    list_display = ('japanese_word', 'kanji_word', 'type', 'meaning')
    list_filter = ('type',)
    search_fields = ['japanese_word', 'kanji_word','meaning']


class ToneAdmin(admin.ModelAdmin):
    list_display = ('hiragana', 'katakana', 'romaji')
    list_filter = ('duan', 'hang', 'type',)


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GrammerAdmin(admin.ModelAdmin):
    list_display = ('grammer', 'chapter')
    list_filter = ('chapter',)


class NovelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class Novel_ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'novel')
    list_filter = ('novel',)


class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist')
    list_filter = ('artist',)


admin.site.register(Type, TypeAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Tone, ToneAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Grammer, GrammerAdmin)
admin.site.register(Novel, NovelAdmin)
admin.site.register(Novel_Chapter, Novel_ChapterAdmin)
admin.site.register(Song, SongAdmin)
