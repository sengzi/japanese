from .models import Type, Chapter, Novel, Song


def nav(request):
    
    type = Type.objects.all()

    for t in type:
        t.name = t.name.split("_")[1]
    
    return {
        'type': type,
        'chapter': Chapter.objects.all(),
        'base_novel': Novel.objects.all(),
        'base_song': Song.objects.all(),
    }
