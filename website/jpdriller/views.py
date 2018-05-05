import random

from django.shortcuts import render

from .models import *


def index(request):
    groups = Vocabulary.objects.values('group').distinct()
    #vocabulary = vocabulary[random.randint(0,len(vocabulary)-1)]
    context = {'groups':groups}
    return render(request, 'jpdriller/index.html',context)