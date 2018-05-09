from django.db import models

class Vocabulary(models.Model):
    id             = models.IntegerField('Identifier',primary_key=True)
    group          = models.CharField('Group',max_length=20)
    vocabulary     = models.CharField('Vocabulary',max_length=20)
    pronounciation = models.CharField('Pronounciation',max_length=20,null=True)
    translation    = models.CharField('Translation',max_length=20)
    note           = models.CharField('Note',max_length=20,null=True)
    
    def __str__(self):
        return self.vocabulary