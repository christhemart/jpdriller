import random

from django.shortcuts import render

from .models import *

from django.http import JsonResponse
from django.http import HttpResponse


def index(request):
    groups = list(Vocabulary.objects.values('group').distinct())
    context = {'groups':groups}
    return render(request, 'jpdriller/index.html',context)
    
def get_vocabulary(request):
    groups = request.GET['groups'].split(',') 
    vocab = Vocabulary.objects.filter(group__in=groups)

    vocab = vocab[random.randint(0,len(vocab)-1)]
    response = str(vocab.vocabulary)+","+str(vocab.pronounciation)+","+str(vocab.translation)
    return HttpResponse(response)