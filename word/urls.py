from django.urls import path
from . import views

urlpatterns = [
    path('', views.word_front_end, name="japanese"),
    path('word/<slug:word_slug>', views.word_details, name='word-detail'),
    path('grammer/<slug:grammer_slug>', views.grammer_details, name='grammer-detail'),
    path('novel/<slug:novel_slug>', views.novel_details, name='novel-detail'),
    path('novel_chapter/<slug:novel_chapter_slug>', views.novel_chapter_details, name='novel-chapter-detail'),
    path('song/<slug:song_slug>', views.song_details, name='song-detail'),
    path('addform/', views.add_word, name="addform"),
    path('tone/', views.fifty_tone, name="tone"),
    path('quiz/', views.quiz_test, name="quiz"),
]
