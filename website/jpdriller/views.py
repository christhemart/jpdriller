import random

from django.http import HttpResponse
from django.shortcuts import render

from .models import *

def index(request):
    groups = list(Vocabulary.objects.values('group').distinct())
    context = {'groups':groups}
    return render(request, 'jpdriller/index.html',context)
    
def get_vocabulary(request):
    groups = request.GET['groups'].split(',') 
    vocab = Vocabulary.objects.filter(group__in=groups)

    vocab = vocab[random.randint(0,len(vocab)-1)]
    response = str(vocab.vocabulary)+','+str(vocab.pronounciation)+','+str(vocab.translation)+','+str(vocab.note)+','+str(vocab.group)
    return HttpResponse(response)