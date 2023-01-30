from http.client import BAD_GATEWAY
from django.shortcuts import render
from django.db.models import Q
from .models import Type, Word, Tone, Chapter, Grammer, Novel, Novel_Chapter, Song
from .forms import AddWordForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.middleware.csrf import get_token
import random
import json

import pandas as pd
import numpy as np
import re

# from django.http import HttpResponse

# Create your views here.


def word_front_end(request):
    type = Type.objects.all()
    chapter = Chapter.objects.all()
    novel = Novel.objects.all()
    song = Song.objects.all()

    for t in type:
        t.name = t.name.split("_")[1]

    return render(request, 'word/index.html', {
        'title': '日语',
        'word_details': type,
        'grammer_datails': chapter,
        'novel_details': novel,
        'song_details': song,
    })


def get_masu_type(selected_word):
    for w in selected_word:
        if(w.kanji_word == 'ー'):
            japanese = w.japanese_word
        else:
            japanese = w.kanji_word

        x = len(w.japanese_word)

        if(w.kanji_word == '滑る'):
            w.masu = '滑ります'
            w.verb_type = '一类'
        elif (w.kanji_word == '知る'):
            w.masu = '知ります'
            w.verb_type = '一类'
        elif (w.kanji_word == '入る'):
            w.masu = '	入ります'
            w.verb_type = '一类'
        elif (w.kanji_word == '切る'):
            w.masu = '	切ります'
            w.verb_type = '一类'
        elif (w.kanji_word == '帰る'):
            w.masu = '	帰ります'
            w.verb_type = '一类'
        elif (w.kanji_word == '来る'):
            w.masu = '	来ます'
            w.verb_type = '三类'
        elif (w.japanese_word[x-2]+w.japanese_word[x-1]) == 'する' and w.japanese_word != "する":
            w.masu = japanese.replace("する", "します")
            w.verb_type = '三类'
        # elif (japanese[x-2]+japanese[x-1]) == 'きる':
        #     w.masu = japanese.replace("きる","きます")
        elif w.japanese_word[x-1] == 'る' and (getduan(w.japanese_word[x-2]) == 'い' or getduan(w.japanese_word[x-2]) == 'え'):
            w.masu = japanese.replace("る", "ます")
            w.verb_type = '二类'
        else:
            masu_hang = gethang(w.japanese_word[x-1])
            if(getword(masu_hang,'い') != None):
                w.masu = japanese.replace(w.japanese_word[x-1], getword(masu_hang,'い')+"ます")
                w.verb_type = '一类'
            else:
                w.masu = '-'     
                w.verb_type = '-'   

    return selected_word


def get_te_type(selected_word):
    try:
        for w in selected_word:
            if(w.kanji_word == 'ー'):
                japanese = w.japanese_word
            else:
                japanese = w.kanji_word

            x = len(w.japanese_word)

            if (w.kanji_word == '来る'):
                w.te_word = '来て'
            elif w.verb_type == '三类':
                w.te_word = japanese.replace("する", "して")
            elif w.verb_type == '二类':
                w.te_word = japanese.replace("る", "て")
            elif w.verb_type == '一类':
                if w.kanji_word == '行く':
                    w.te_word = '行って'
                elif w.japanese_word[x-1] == 'う' or w.japanese_word[x-1] == 'つ' or w.japanese_word[x-1] == 'る':
                    w.te_word = japanese.replace(w.japanese_word[x-1], "って")
                elif w.japanese_word[x-1] == 'む' or w.japanese_word[x-1] == 'ぶ' or w.japanese_word[x-1] == 'ぬ':
                    w.te_word = japanese.replace(w.japanese_word[x-1], "んで")
                elif w.japanese_word[x-1] == 'く':
                    w.te_word = japanese.replace(w.japanese_word[x-1], "いて")
                elif w.japanese_word[x-1] == 'ぐ':
                    w.te_word = japanese.replace(w.japanese_word[x-1], "いで")
                elif w.japanese_word[x-1] == 'す':
                    w.te_word = japanese.replace(w.japanese_word[x-1], "して")
            else:
                w.te_word = '-'   

        return selected_word

    except Exception as exc:
        print(exc)


def get_nai_type(selected_word):
    try:
        for w in selected_word:
            if(w.kanji_word == 'ー'):
                japanese = w.japanese_word
            else:
                japanese = w.kanji_word

            x = len(w.japanese_word)

            if (w.kanji_word == '来る'):
                w.ne_word = '来ない'
            elif (w.japanese_word == 'ある'):
                w.ne_word = 'ない'
            elif w.verb_type == '三类':
                w.ne_word = japanese.replace("する", "しない")
            elif w.verb_type == '二类':
                w.ne_word = japanese.replace("る", "ない")
            elif w.verb_type == '一类':
                masu_hang = gethang(w.japanese_word[x-1])
                
                if w.japanese_word[x-1] == 'う':
                    w.ne_word = japanese.replace(w.japanese_word[x-1], "わない")
                elif(getword(masu_hang,'あ') != None):
                    w.ne_word = japanese.replace(w.japanese_word[x-1], getword(masu_hang,'あ')+"ない")
                else:
                    w.ne_word = '-'     

        return selected_word

    except Exception as exc:
        print(exc)


def get_ta_type(selected_word):
    try:
        for w in selected_word:
            if(w.kanji_word == 'ー'):
                japanese = w.japanese_word
            else:
                japanese = w.kanji_word

            x = len(w.japanese_word)

            if (w.kanji_word == '来る'):
                w.ta_word = '来た'
            elif w.verb_type == '三类':
                w.ta_word = japanese.replace("する", "した")
            elif w.verb_type == '二类':
                w.ta_word = japanese.replace("る", "た")
            elif w.verb_type == '一类':
                if w.kanji_word == '行く':
                    w.ta_word = '行った'
                elif w.japanese_word[x-1] == 'う' or w.japanese_word[x-1] == 'つ' or w.japanese_word[x-1] == 'る':
                    w.ta_word = japanese.replace(w.japanese_word[x-1], "った")
                elif w.japanese_word[x-1] == 'む' or w.japanese_word[x-1] == 'ぶ' or w.japanese_word[x-1] == 'ぬ':
                    w.ta_word = japanese.replace(w.japanese_word[x-1], "んだ")
                elif w.japanese_word[x-1] == 'く':
                    w.ta_word = japanese.replace(w.japanese_word[x-1], "いた")
                elif w.japanese_word[x-1] == 'ぐ':
                    w.ta_word = japanese.replace(w.japanese_word[x-1], "いだ")
                elif w.japanese_word[x-1] == 'す':
                    w.ta_word = japanese.replace(w.japanese_word[x-1], "した")
            else:
                w.ta_word = '-'   

        return selected_word

    except Exception as exc:
        print(exc)


def get_meirei_type(selected_word):
    for w in selected_word:
        if(w.kanji_word == 'ー'):
            japanese = w.japanese_word
        else:
            japanese = w.kanji_word

        x = len(w.japanese_word)

        if w.verb_type == '三类':
            w.meirei = japanese.replace("する", "しろ")
        elif w.verb_type == '二类':
            w.meirei = japanese.replace("る", "ろ")
        elif w.verb_type == '一类':
            meirei_hang = gethang(w.japanese_word[x-1])
            if(getword(meirei_hang,'え') != None):
                w.meirei = japanese.replace(w.japanese_word[x-1], getword(meirei_hang,'え'))
            else:
                w.meirei = '-'     
                w.verb_type = '-'  
            
    return selected_word


def get_ishi_type(selected_word):
    for w in selected_word:
        if(w.kanji_word == 'ー'):
            japanese = w.japanese_word
        else:
            japanese = w.kanji_word

        x = len(w.japanese_word)

        if w.verb_type == '三类':
            w.ishi = japanese.replace("する", "しよう")
        elif w.verb_type == '二类':
            w.ishi = japanese.replace("る", "よう")
        elif w.verb_type == '一类':
            ishi_hang = gethang(w.japanese_word[x-1])
            if(getword(ishi_hang,'お') != None):
                w.ishi = japanese.replace(w.japanese_word[x-1], getword(ishi_hang,'お')+"う")
                w.verb_type = '一类'
            else:
                w.ishi = '-'     
                w.verb_type = '-'   

    return selected_word


def get_ba_type(selected_word):
    for w in selected_word:
        if(w.kanji_word == 'ー'):
            japanese = w.japanese_word
        else:
            japanese = w.kanji_word

        x = len(w.japanese_word)

        if w.verb_type == '三类':
            w.ba_word = japanese.replace("する", "すれば")
        elif w.verb_type == '二类':
            w.ba_word = japanese.replace("る", "れば")
        elif w.verb_type == '一类':
            ba_word_hang = gethang(w.japanese_word[x-1])
            if(getword(ba_word_hang,'え') != None):
                w.ba_word = japanese.replace(w.japanese_word[x-1], getword(ba_word_hang,'え')+"ば")
                w.verb_type = '一类'
            else:
                w.ba_word = '-'     
                w.verb_type = '-'   

    return selected_word


def get_kano_type(selected_word):
    for w in selected_word:
        if(w.kanji_word == 'ー'):
            japanese = w.japanese_word
        else:
            japanese = w.kanji_word

        x = len(w.japanese_word)

        if w.verb_type == '三类':
            w.kano = japanese.replace("する", "できる")
        elif w.verb_type == '二类':
             w.kano = japanese.replace("る", "られる")
        elif w.verb_type == '一类':
            kano_hang = gethang(w.japanese_word[x-1])
            if(getword(kano_hang,'え') != None):
                w.kano = japanese.replace(w.japanese_word[x-1], getword(kano_hang,'え')+"る")
                w.verb_type = '一类'
            else:
                w.kano = '-'     
                w.verb_type = '-'   

    return selected_word


def get_passive_type(selected_word):
    for w in selected_word:
        if(w.kanji_word == 'ー'):
            japanese = w.japanese_word
        else:
            japanese = w.kanji_word

        x = len(w.japanese_word)

        if w.verb_type == '三类':
            w.passive = japanese.replace("する", "される")
        elif w.verb_type == '二类':
             w.passive = japanese.replace("る", "られる")
        elif w.verb_type == '一类':
            passive_hang = gethang(w.japanese_word[x-1])
            if(getword(passive_hang,'あ') != None):
                w.passive = japanese.replace(w.japanese_word[x-1], getword(passive_hang,'あ')+"れる")
                w.verb_type = '一类'
            else:
                w.passive = '-'     
                w.verb_type = '-'   

    return selected_word


def getduan(w):
    try:
        return Tone.objects.get(hiragana=w).duan
    except Exception as exc:
        print(w)


def gethang(w):
    try:
        return Tone.objects.get(hiragana=w).hang
    except Exception as exc:
        print(w)


def getword(masu_hang,duan):
    try:
        word = Tone.objects.filter(hang=masu_hang)

        for w in word:
            if(w.duan == duan):
                return w.hiragana

    except Exception as exc:
        print(exc)


def get_adjective_type(selected_word):
    
    try:
        for w in selected_word:
            if(w.kanji_word == 'ー'):
                japanese = w.japanese_word
            else:
                japanese = w.kanji_word

            x = len(japanese)

            if japanese == '嫌い':
                w.adjective_type = '二类'
            elif japanese[x-1] == 'い':
                w.adjective_type = '一类'
            else:
                w.adjective_type = '二类'

        return selected_word

    except Exception as exc:
        print(exc)


def word_details(request, word_slug):

    try:
        
        if(word_slug == 'all'):
            selected_type = "所有日文"
            search = request.GET.get('search')

            if search == None:
                selected_word = Word.objects.all().order_by('id')
                search = ""
            else:
                selected_word = Word.objects.filter(Q(meaning__contains=search) | Q(kanji_word__contains=search) | Q(japanese_word__contains=search)).order_by('id')

        else:
            selected_type = Type.objects.get(slug=word_slug)

            selected_type.name = selected_type.name.split("_")[1]
            
            search = request.GET.get('search')
            if search == None:
                selected_word = Word.objects.filter(type=selected_type).order_by('id')
                search = ""
            else:
                selected_word = Word.objects.filter(Q(type=selected_type) & (Q(meaning__contains=search) | Q(kanji_word__contains=search) | Q(japanese_word__contains=search))).order_by('id')

        all_type = list(Type.objects.all())

        if word_slug == 'verb':
            selected_word = get_masu_type(selected_word)
            selected_word = get_te_type(selected_word)
            selected_word = get_nai_type(selected_word)   
            selected_word = get_ta_type(selected_word)
            selected_word = get_meirei_type(selected_word)
            selected_word = get_ishi_type(selected_word)
            selected_word = get_ba_type(selected_word)
            selected_word = get_kano_type(selected_word)
            selected_word = get_passive_type(selected_word)
        elif word_slug == 'adjective':
            selected_word = get_adjective_type(selected_word)

        # pagination
        p = Paginator(selected_word, 20)
        page_number = request.GET.get('page')

        for sw in selected_word:
            sw.type.name = sw.type.name.split("_")[1]

        if page_number == "":
            page_obj = p.get_page(1)
        else:
            page_obj = p.get_page(page_number)

        # add word
        # if request.method == 'POST':
        #     add_form = AddWordForm(request.POST)
        #     if add_form.is_valid():
        #         word = add_form.save()

        return render(request, 'word/word-details.html', {
            'error': False,
            'type_name': selected_type,
            'word': page_obj,
            'all_type': all_type,
            'slug': word_slug,
            'search': search
        })
    except Exception as exc:
        return render(request, 'word/word-details.html', {
            'error': True,
        })


def add_word(request):

    if request.method == 'GET':
        add_form = AddWordForm()
        return render(request, 'word/add-word.html', {
            'form': add_form
        })
    else:
        add_form = AddWordForm(request.POST)
        if add_form.is_valid():
            word = add_form.save()

            selected_type = Type.objects.get(name=word.type)
            selected_word = Word.objects.filter(type=selected_type)

            return render(request, 'word/word-details.html', {
                'error': False,
                'type_name': selected_type,
                'word': selected_word,
            })


def arrange_tone(hang, tones):

    hika_tones_array = []
    kata_tones_array = []

    for h in hang:

        hira = list(x for x in tones[tones['hang'] == h].hiragana)
        romaji = list(x for x in tones[tones['hang'] == h].romaji)
        kata = list(x for x in tones[tones['hang'] == h].katakana)
        hira_array = []
        kata_array = []
        duan = sorted(list(x for x in tones[tones['hang'] == h].duan))

        num = 0
        x = 0

        while num < 5:
            if duan[num] == 'あ' and x == 0:
                hira_array.append(hira[num]+' ('+romaji[num]+')')
                kata_array.append(kata[num]+' ('+romaji[num]+')')
                num += 1
            elif duan[num] == 'い' and x == 1:
                hira_array.append(hira[num]+' ('+romaji[num]+')')
                kata_array.append(kata[num]+' ('+romaji[num]+')')
                num += 1
            elif duan[num] == 'う' and x == 2:
                hira_array.append(hira[num]+' ('+romaji[num]+')')
                kata_array.append(kata[num]+' ('+romaji[num]+')')
                num += 1
            elif duan[num] == 'え' and x == 3:
                hira_array.append(hira[num]+' ('+romaji[num]+')')
                kata_array.append(kata[num]+' ('+romaji[num]+')')
                num += 1
            elif duan[num] == 'お' and x == 4:
                hira_array.append(hira[num]+' ('+romaji[num]+')')
                kata_array.append(kata[num]+' ('+romaji[num]+')')
                break
            else:
                hira_array.append('')
                kata_array.append('')

            x += 1

        hika_tones_array.append(hira_array)
        kata_tones_array.append(kata_array)

    return [hika_tones_array, kata_tones_array]


def fifty_tone(request):

    tones = pd.DataFrame(list(Tone.objects.filter(type='五十音').values()))
    voiced = pd.DataFrame(list(Tone.objects.filter(type='浊音').values()))
    hang = list(h for h in pd.unique(tones['hang']))
    voiced_hang = list(h for h in pd.unique(voiced['hang']))

    fifty_array = arrange_tone(hang, tones)
    voiced_array = arrange_tone(voiced_hang, voiced)

    hika_tones_array = fifty_array[0]
    kata_tones_array = fifty_array[1]

    voiced_hika_tones_array = voiced_array[0]
    voiced_kata_tones_array = voiced_array[1]

    return render(request, 'word/50-tone.html', {
        'title': '五十音',
        'hira_tone': hika_tones_array,
        'kata_tone': kata_tones_array,
        'voiced_hika': voiced_hika_tones_array,
        'voiced_kata': voiced_kata_tones_array,
    })


def getRomaji(w):
    try:
        if(w == 'ー'):
            return 'ー '
        else:
            return Tone.objects.get(hiragana=w).romaji+' '
    except Tone.DoesNotExist:
        return Tone.objects.get(katakana=w).romaji+' '


def grammer_details(request, grammer_slug):
    try:
        if grammer_slug != 'other':
            selected_chapter = Chapter.objects.get(slug=grammer_slug)
            selected_grammer = Grammer.objects.filter(chapter=selected_chapter)
            basic_image = Chapter.objects.get(slug=grammer_slug).basic_image
            dialog_image = Chapter.objects.get(slug=grammer_slug).dialog_image
            max_chapter = Chapter.objects.all().count()

            previous_chapter = selected_chapter.id - 1
            next_chapter = selected_chapter.id + 1

            if selected_chapter.id == max_chapter:
                next_chapter = 0
                previous_chapter = Chapter.objects.get(id=previous_chapter).slug
            elif selected_chapter.id == 1:
                next_chapter = Chapter.objects.get(id=next_chapter).slug
                previous_chapter = 0
            else:
                next_chapter = Chapter.objects.get(id=next_chapter).slug
                previous_chapter = Chapter.objects.get(id=previous_chapter).slug
        else:
            selected_chapter = '额外知识'
            selected_grammer = ''
            previous_chapter = 0
            next_chapter = 0
            basic_image = ''
            dialog_image = ''

        if request.method == 'POST':
            meaning = Word.objects.get(kanji_word=request.POST['word']).meaning
            word = Word.objects.get(
                kanji_word=request.POST['word']).japanese_word
            string = ""

            num = 0
            remove_num = []

            tsu_check = False

            for w in word:
                if w == 'ゃ' or w == 'ゅ' or w == 'ょ' or w == 'ャ' or w == 'ュ' or w == 'ョ':
                    string += getRomaji(word[num-1] + w)
                    remove_num.append(num-1)
                elif w == 'っ':
                    tsu_check = True
                else:
                    if tsu_check:
                        string += getRomaji(w)[0] + getRomaji(w)
                        tsu_check = False
                    else:
                        string += getRomaji(w)

                num = num + 1

            list_string = string.split()

            for n in remove_num:
                string = string.replace(list_string[n]+" ", "")

            return HttpResponse([meaning, ',', word, ',', string])

        else:
            return render(request, 'word/grammer-details.html', {
                'chapter_name': selected_chapter,
                'grammer': selected_grammer,
                'slug': grammer_slug,
                'previous_chapter': previous_chapter,
                'next_chapter': next_chapter,
                'basic_image': basic_image,
                'dialog_image': dialog_image,
                'error': False,
            })
    except Word.DoesNotExist:
        try:
            meaning = Word.objects.get(
                japanese_word=request.POST['word']).meaning
            word = Word.objects.get(
                japanese_word=request.POST['word']).japanese_word
            string = ""

            for w in word:
                string += getRomaji(w)

            return HttpResponse([meaning, ',', word, ',', string])

        except Word.DoesNotExist:
            return HttpResponse("")

    except Exception as exc:
        return render(request, 'word/grammer-details.html', {
            'error': True,
        })


def quiz_test(request):
    try:
        word = list(Word.objects.all())
        random_word = random.sample(word, 20)

        return render(request, 'word/quiz.html', {
            'error': False,
            'title': '测验',
            'word': random_word
        })
    except Exception as exc:
        return render(request, 'word/quiz.html', {
            'error': True,
        })


def novel_details(request, novel_slug):

    try:
        
        selected_novel = Novel.objects.get(slug=novel_slug)
        selected_novel_chapter = Novel_Chapter.objects.filter(novel=selected_novel)
        
        return render(request, 'word/novel-details.html', {
            'error': False,
            'novel': selected_novel,
            'novel_chapter': selected_novel_chapter,
        })
    except Exception as exc:
        return render(request, 'word/novel-details.html', {
            'novel': selected_novel,
            'error': True,
        })


def song_details(request, song_slug):

    try:
        song_name = Song.objects.get(slug=song_slug).name
        content = Song.objects.get(slug=song_slug).content
        meaning = Song.objects.get(slug=song_slug).meaning
        link = Song.objects.get(slug=song_slug).link
        artist = Song.objects.get(slug=song_slug).artist
        content_array = content.split('\r\n')
        meaning_array = meaning.split('\r\n')

        find_kanji_hiragana(content_array)
        
        return render(request, 'word/song-details.html', {
            'error': False,
            'song': song_name,
            'content': content_array,
            'meaning': meaning_array,
            'link': link,
            'artist': artist
        })
    except Exception as exc:
        return render(request, 'word/song-details.html', {
            'error': True,
        })


def novel_chapter_details(request, novel_chapter_slug):
    try:
        
        if request.method == "POST":
            w = request.POST.get('word','')
            word = request.POST.get('sentence','')
            count = 0
            definition = []

            change_kanji(w,word,count,definition)

            return HttpResponse(json.dumps({
                "w": definition[0],
                "meaning": definition[1],
                "type": definition[2],
                "kanji": definition[3],
                "hiragana": definition[4]
            }), content_type="application/json")
        
        novel = novel_chapter_slug.split("_")
        novel_name = '_'.join(novel[:len(novel)-1])
        novel_id = Novel.objects.get(slug=novel_name).id

        chapter = int(novel[len(novel)-1])
        max_chapter = Novel_Chapter.objects.filter(novel_id=novel_id).count()

        chapter_name = Novel_Chapter.objects.get(slug=novel_chapter_slug).name
        content = Novel_Chapter.objects.get(slug=novel_chapter_slug).content
        content_array2 = Novel_Chapter.objects.get(slug=novel_chapter_slug).content
        meaning = Novel_Chapter.objects.get(slug=novel_chapter_slug).meaning
        content_array = content.replace('\r\n\r\n\r\n\r\n\r\n',"\r\n\r\n")
        content_array = content_array.replace('\r\n\r\n\r\n\r\n',"\r\n\r\n")
        content_array = content_array.replace('\r\n\r\n\r\n',"\r\n\r\n")
        content_array = content_array.split('\r\n')

        previous_chapter = chapter - 1
        next_chapter = chapter + 1

        if chapter == 1 and chapter == max_chapter:
            next_chapter = 0
            previous_chapter = 0
        elif chapter == 1:
            next_chapter = Novel_Chapter.objects.get(id=next_chapter).slug
            previous_chapter = 0
        elif chapter == max_chapter:
            next_chapter = 0
            previous_chapter = Novel_Chapter.objects.get(id=previous_chapter).slug
        else:
            next_chapter = Novel_Chapter.objects.get(id=next_chapter).slug
            previous_chapter = Novel_Chapter.objects.get(id=previous_chapter).slug

        find_kanji_hiragana(content_array)
     
        return render(request, 'word/novel-chapter-details.html', {
            'error': False,
            'chapter_name': chapter_name,
            'content': content_array,
            'content2': content_array2,
            'meaning': meaning,
            'next_chapter': next_chapter,
            'previous_chapter': previous_chapter,
            'slug': novel_chapter_slug,
            'csrftoken': get_token(request)
            
        })
    except Exception as exc:
        print(exc)
        return render(request, 'word/novel-chapter-details.html', {
            'error': True,
        })


def find_kanji_hiragana(content_array):
    
    count = 0

    for word in content_array:
        count = count + 1

        if word != "":
            changed_word = []

            for w in re.findall('[\u4e00-\u9fa5]+', word):
                change_kanji(w,word,count,changed_word)

            word_dict = {}
            for num in range(len(changed_word)):
                if num % 2 == 0 or num == 0:
                    
                    if changed_word[num+1] in list(word_dict.keys()):
                        word_dict[changed_word[num+1] + str(num)] = changed_word[num]
                    else:
                        word_dict[changed_word[num+1]] = changed_word[num]


            for k in sorted(word_dict, key=lambda k: len(word_dict[k]), reverse=True):

                new_word = ""
                i = 0
                try:
                    for c_a in content_array[count-1].split(word_dict[k]):
                        i += 1

                        if i == len(content_array[count-1].split(word_dict[k])):
                            new_word += c_a
                            i = 0
                        else:
                            if content_array[count-1].split(word_dict[k])[i] == "" or c_a == "":
                                wd = word_dict[k]
                                k = ''.join([i for i in k if not i.isdigit()])
                                new_word +=  c_a + "<ruby><rb>"+wd+"</rb><rt>"+k+"</rt></ruby>"
                            else:

                                condition1 = (c_a[-7:] != "</ruby>" or c_a[-7:] == "</ruby>")
                                condition2 = c_a[-4:] != "<rb>"
                                condition3 = (content_array[count-1].split(word_dict[k])[i][0] != "<" or content_array[count-1].split(word_dict[k])[i][:6] == "<ruby>")
                                condition4 = (not re.findall('[\u4e00-\u9fa5]+', c_a[-1]) or not re.findall('[\u4e00-\u9fa5]+',content_array[count-1].split(word_dict[k])[i][0])) or c_a[-2] != ">"

                                if condition1 and condition2 and condition3 and condition4:
                                    wd = word_dict[k]
                                    k = ''.join([i for i in k if not i.isdigit()])
                                    new_word +=  c_a + "<ruby><rb>"+wd+"</rb><rt>"+k+"</rt></ruby>"
                                    
                                elif c_a[-1] == ">" or re.findall('[\u4e00-\u9fa5]+', c_a[-1]):
                                    new_word += c_a + word_dict[k]
                                else:
                                    new_word +=  c_a
                                
                    content_array[count-1] = new_word
                except Exception as exc:
                    print(exc)
                    print(word_dict[k])
                    print(count)
                    continue

def change_kanji(w,word,count,changed_word):
    
    try:
        kanji = Word.objects.filter(Q(kanji_word__contains=w)).order_by('type__name')
        
        if w == "":
            return False

        if kanji:

            for k in kanji:

                if k.type.name == "1_动词" and k.kanji_word.find(w) == 0:
                    
                    change_verb = [k]
                    change_verb = get_masu_type(change_verb)
                    change_verb = get_te_type(change_verb)
                    change_verb = get_nai_type(change_verb)   
                    change_verb = get_ta_type(change_verb)
                    change_verb = get_meirei_type(change_verb)
                    change_verb = get_ishi_type(change_verb)
                    change_verb = get_ba_type(change_verb)
                    change_verb = get_kano_type(change_verb)
                    change_verb = get_passive_type(change_verb)

                    masu = change_verb[0].masu.replace('ます','').strip()
                    te_word = change_verb[0].te_word.strip()
                    ne_word = change_verb[0].ne_word.strip()
                    ta_word = change_verb[0].ta_word.strip()
                    meirei = change_verb[0].meirei.strip()
                    ishi = change_verb[0].ishi.strip()
                    ba_word = change_verb[0].ba_word.strip()
                    kano = change_verb[0].kano.strip()
                    passive = change_verb[0].passive.strip()

                    condition0 = word.find(k.kanji_word) != -1
                    condition1 = word.find(masu) != -1
                    condition2 = word.find(te_word) != -1
                    condition3 = word.find(ne_word) != -1
                    condition4 = word.find(ta_word) != -1
                    condition5 = word.find(meirei) != -1
                    condition6 = word.find(ishi) != -1
                    condition7 = word.find(ba_word) != -1
                    condition8 = word.find(kano) != -1
                    condition9 = word.find(passive) != -1
                    condition10 = word.find(te_word.replace('て','')) != -1 or word.find(te_word.replace('で','')) != -1
                    condition11 = word.find(kano.replace('れる','れて')) != -1
                    condition12 = word.find(passive.replace('れる','れて')) != -1
                    condition13 = word.find(ne_word.replace('ない','')) != -1
                    condition14 = word.find(k.kanji_word.replace('する','')) != -1
                    condition15 = word.find(k.kanji_word.replace('くる','')) != -1
                    condition16 = word.find(kano.replace('れる','')) != -1

                    if condition0 or condition1 or condition2 or condition3 or condition4 or condition5 or condition6 or condition7 or condition8 or condition9 or condition10 or condition11 or condition12 or condition13 or condition14 or condition15 or condition16:
                        
                        if condition14:
                            w = k.kanji_word.replace('する','')

                        contain_kanji = re.findall('[\u4e00-\u9fa5]+', k.kanji_word)
                        remove_hiragana = re.findall('[\u30a0-\u30ff\u3040-\u309f]+', k.kanji_word)
                        remove_kanji_hiragana = re.findall('[\u30a0-\u30ff\u3040-\u309f]+', w)
                        kanji_hiragana = k.japanese_word

                        if len(contain_kanji) > 1:
                            for x in range(len(contain_kanji)):
                                kw = k.kanji_word
                                
                                if x+1 == len(contain_kanji):
                                    hiragana = kanji_hiragana.split(k.kanji_word.split(contain_kanji[x])[-1])[0]
                                    w = k.kanji_word[:-1]
                                else: 
                                    hiragana = kanji_hiragana.split(k.kanji_word.split(contain_kanji[x+1])[0][-1])[0]
                                    w = k.kanji_word.split(contain_kanji[x+1])[0][:-1]

                                    kanji_hiragana = kanji_hiragana.replace(hiragana+k.kanji_word.split(contain_kanji[x+1])[0][-1],"")
                                    k.kanji_word = k.kanji_word.replace(k.kanji_word.split(contain_kanji[x+1])[0],"")
                                    
                                if w not in changed_word :
                                    if hiragana.find('/'):
                                        hiragana = hiragana.split('/')[0]

                                    if count == 0:
                                        changed_word.append(w)
                                        changed_word.append(k.meaning)
                                        changed_word.append(k.type.name)
                                        changed_word.append(kw)
                                        changed_word.append(k.japanese_word)
                                    else:
                                        changed_word.append(w)
                                        changed_word.append(hiragana)       
                            return True
                        else:
                            if len(remove_hiragana[0]) == 1 and change_verb[0].verb_type == "一类":
                                kanji_hiragana = kanji_hiragana[:-1]
                            else: 
                                if remove_hiragana:
                                    for rh in remove_hiragana:
                                        kanji_hiragana = kanji_hiragana.replace(rh, '')

                            if remove_kanji_hiragana:
                                for rkh in remove_kanji_hiragana:
                                    w = w.replace(rkh, '')

                            if w not in changed_word :
                                if kanji_hiragana.find('/'):
                                    kanji_hiragana = kanji_hiragana.split('/')[0]

                                if count == 0:
                                    changed_word.append(w)
                                    changed_word.append(k.meaning)
                                    changed_word.append(k.type.name)
                                    changed_word.append(k.kanji_word)
                                    changed_word.append(k.japanese_word)
                                else:
                                    changed_word.append(w)
                                    changed_word.append(kanji_hiragana)
                                return True
                            
                elif k.type.name == "2_形容词" and k.kanji_word.find(w) == 0:
                    
                    condition0 = word.find(k.kanji_word) != -1
                    condition1 = word.find(k.kanji_word.replace('い','')) != -1

                    if condition0 or condition1:
                        remove_hiragana = re.findall('[\u30a0-\u30ff\u3040-\u309f]+', k.kanji_word)
                        remove_kanji_hiragana = re.findall('[\u30a0-\u30ff\u3040-\u309f]+', w)
                        
                        kanji_hiragana = k.japanese_word    

                        if remove_hiragana:
                            for rh in remove_hiragana:
                                if remove_hiragana[0] == 'い':
                                    kanji_hiragana = kanji_hiragana[:-1]
                                else:
                                    kanji_hiragana = kanji_hiragana.replace(rh, '')

                        if remove_kanji_hiragana:
                            for rkh in remove_kanji_hiragana:
                                w = w.replace(rkh, '')

                        if w not in changed_word :
                            if kanji_hiragana.find('/'):
                                kanji_hiragana = kanji_hiragana.split('/')[0]

                            if count == 0:
                                changed_word.append(w)
                                changed_word.append(k.meaning)
                                changed_word.append(k.type.name)
                                changed_word.append(k.kanji_word)
                                changed_word.append(k.japanese_word)
                            else:
                                changed_word.append(w)
                                changed_word.append(kanji_hiragana)
                            return True
                
                # elif word[int(word.find(w))-1:word.find(w)] == "お":
                #     change_kanji("お"+w,word,count,changed_word)

                elif k.kanji_word.find(w) == 0:

                    if word.find(k.kanji_word) != -1:
                        
                        w = k.kanji_word
                        remove_hiragana = re.findall('[\u30a0-\u30ff\u3040-\u309f]+', k.kanji_word)
                        remove_kanji_hiragana = re.findall('[\u30a0-\u30ff\u3040-\u309f]+', w)

                        kanji_hiragana = k.japanese_word

                        if remove_hiragana:
                            for rh in remove_hiragana:
                                kanji_hiragana = kanji_hiragana.replace(rh, '')

                        if remove_kanji_hiragana:
                            for rkh in remove_kanji_hiragana:
                                w = w.replace(rkh, '')

                        if w not in changed_word :
                            if kanji_hiragana.find('/'):
                                kanji_hiragana = kanji_hiragana.split('/')[0]

                            if count == 0:
                                changed_word.append(w)
                                changed_word.append(k.meaning)
                                changed_word.append(k.type.name)
                                changed_word.append(k.kanji_word)
                                changed_word.append(k.japanese_word)
                            else:
                                changed_word.append(w)
                                changed_word.append(kanji_hiragana)
                            return True
                            
        else:
            if len(w) > 1:
                change_kanji(w[:-1],word,count,changed_word)
                change_kanji(w.replace(w[:-1],''),word,count,changed_word)

                if w[:-1] not in changed_word and w.replace(w[:-1],'') not in changed_word:
                    change_kanji(w[1:],word,count,changed_word)
                    change_kanji(w.replace(w[1:],''),word,count,changed_word)

                for change in changed_word:
                    if w.find(change) != -1:
                        w = w.replace(change,'')
                        if w:
                            change_kanji(w,word,count,changed_word)
        
        return False

    except Exception as exc:
        # print(exc)
        # print(w)
        # print(count)
        return False

    
    