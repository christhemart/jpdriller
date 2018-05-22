import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import *


def index(request):
    groups = list(Vocabulary.objects.values('group').distinct())
    if request.user.is_authenticated:
        context = {'groups': groups, 'user': request.user}
    else:
        context = {'groups': groups, 'user': None}
    return render(request, 'jpdriller/index.html', context)


def login_view(request):
    username = request.POST.get('login-username', None)
    password = request.POST.get('login-password', None)
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
    return redirect('')


def logout_view(request):
    logout(request)
    return redirect('')


def register_view(request):
    username = request.POST.get('register-username', None)
    password = request.POST.get('register-password', None)
    user = User.objects.create_user(username=username, password=password)
    user.save()
    login(request, user)
    return redirect('')


def get_vocabulary(request):
    groups = request.GET['groups'].split(',')
    vocab = Vocabulary.objects.filter(group__in=groups)

    vocab = vocab[random.randint(0, len(vocab) - 1)]

    if request.user.is_authenticated:
        try:
            stat = UserVocabStats.objects.get(user__exact=request.user, vocabulary__exact=vocab)
        except UserVocabStats.DoesNotExist:
            stat = UserVocabStats()
            stat.id = UserVocabStats.objects.all().aggregate(Max('id'))['id__max'] + 1
            stat.user = request.user
            stat.vocabulary = vocab
            stat.count = 0
            stat.streak = 0
            stat.save()
    else:
        stat = None

    if str(vocab.group) not in ['Hiragana', 'Katakana']:
        response = str(random.randint(0, 1))
    else:
        response = '0'

    response += ',' + str(vocab.id) + ',' + str(vocab.vocabulary) + ',' + str(vocab.pronunciation) + ',' + str(
        vocab.translation) + ',' + str(vocab.note) + ',' + str(vocab.group) + ','

    if stat:
        response += str(stat.streak)
    else:
        response += ''

    return HttpResponse(response)


def stat_update(request):
    success = request.GET['success']
    vocab_id = request.GET['vocabid']
    vocab = Vocabulary.objects.get(id__exact=vocab_id)

    stat = UserVocabStats.objects.get(user__exact=request.user, vocabulary__exact=vocab)

    if int(success):
        stat.count += 1
        stat.streak += 1
    else:
        stat.streak = 0

    stat.save()

    return HttpResponse('')
