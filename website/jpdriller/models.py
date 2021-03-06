from django.contrib.auth.models import User
from django.db import models


class Vocabulary(models.Model):
    id = models.IntegerField('Identifier', primary_key=True)
    group = models.CharField('Group', max_length=20)
    vocabulary = models.CharField('Vocabulary', max_length=20)
    pronunciation = models.CharField('Pronunciation', max_length=20, null=True)
    translation = models.CharField('Translation', max_length=20)
    note = models.CharField('Note', max_length=20, null=True)

    def __str__(self):
        return self.vocabulary


class UserVocabStats(models.Model):
    id = models.IntegerField('Identifier', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    count = models.IntegerField('Count')
    streak = models.IntegerField('Streak')

    def __str__(self):
        return str(self.vocabulary)


class UserSettings(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    weight = models.IntegerField('Against')
    cutoff = models.IntegerField('Cutoff')
    selection = models.CharField('Selection', max_length=1000, null=True)
    last_vocab = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)
