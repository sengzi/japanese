from django import forms
from .models import Word

class AddWordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['japanese_word','kanji_word','type','meaning']