from django.shortcuts import render
from . models import Video, Model_weight, Output
from django.shortcuts import HttpResponse
from . forms import Video_form
from . import main

def index(request):
    video = Video.objects.all()
    if request.method == 'POST':
        form = Video_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()  
    else:
        form = Video_form()
    context = {
        'video':video,
        'form': form,
    }
    return render(request, 'index.html', context)

def home(request):
    imgg = Output.objects.all()
    video = Video.objects.all()
    if request.method == 'POST':
        vid = request.POST['caption']
        vi  = Video.objects.get(caption = vid)
        vi_path = vi.Video.path
        detect = main.main(vid_path=vi_path)
        print(detect,'................................')
        for img in detect:
            Output.objects.create(name=vid, image=img)

        context = {
            'video':video,
            'img':imgg
        }
    else:
        context = {
            'video':video,
        }

    return render(request, 'home.html',context)





        
    

