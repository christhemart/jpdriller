import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import *


def index(request):
    groups = list(Vocabulary.objects.values('group').distinct())
    if request.user.is_authenticated:
        settings = UserSettings.objects.get(user__exact=request.user)
        context = {'groups': groups, 'user': request.user, 'settings': settings}
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
    if request.user.is_authenticated:
        logout(request)
    return redirect('')


def register_view(request):
    username = request.POST.get('register-username', None)
    password = request.POST.get('register-password', None)

    if len(password) >= 8 and len(username) >= 4:
        try:
            user = User.objects.create_user(username=username, password=password)

            if user:
                user.save()

                settings = UserSettings()
                settings.user = user
                settings.weight = 5
                settings.cutoff = 10
                settings.save()

                login(request, user)
                return redirect('')
        except IntegrityError:
            pass
    return redirect('naughty')


def check_username(request):
    try:
        User.objects.get(username__exact=request.GET['username'])
        response = 1
    except User.DoesNotExist:
        response = 0
    return HttpResponse(response)


def get_vocabulary(request):
    groups = request.GET['groups']

    if groups == 'GETLAST':
        vocab = UserSettings.objects.get(user__exact=request.user).last_vocab
    else:
        groups = groups.split(',')
        vocab = Vocabulary.objects.filter(group__in=groups)

        if request.user.is_authenticated and random.randint(1, 10) < 10:
            settings = UserSettings.objects.get(user__exact=request.user)
            if settings.cutoff > 0:
                stats = UserVocabStats.objects.filter(user__exact=request.user, vocabulary__in=vocab)
                try:
                    temp = vocab.exclude(id__in=stats.filter(streak__gt=settings.cutoff).values_list('vocabulary'))
                    if len(temp) > 0:
                        vocab = temp
                except vocab.DoesNotExist:
                    pass

        vocab = vocab[random.randint(0, len(vocab) - 1)]

        if request.user.is_authenticated:
            settings = UserSettings.objects.get(user__exact=request.user)
            settings.last_vocab = vocab
            settings.save()

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
        if request.user.is_authenticated:
            settings = UserSettings.objects.get(user__exact=request.user)
            response = '1' if random.randint(1, 10) <= settings.weight else '0'
        else:
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
    if request.user.is_authenticated:
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


def save_settings(request):
    if request.user.is_authenticated:
        weight = request.POST.get('weight', None)
        cutoff = request.POST.get('cutoff', None)

        settings = UserSettings.objects.get(user__exact=request.user)
        settings.weight = weight
        settings.cutoff = cutoff
        settings.save()

    return redirect('')


def save_groups(request):
    if request.user.is_authenticated:
        settings = UserSettings.objects.get(user__exact=request.user)
        settings.selection = request.GET['groups']
        settings.save()

    return HttpResponse('')


def naughty(request):
    response = '<body style="background-color: black; display: flex; justify-content: center; align-items: center;">'
    response += '<br><b><span style="font-size: 72px; color: red;">ヾ( ･`⌓´･)ﾉﾞ</span></b>'
    response += '</body>'
    return HttpResponse(response)
