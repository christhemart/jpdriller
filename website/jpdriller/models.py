from django.db import models

class Hiragana(models.Model):
    id = models.IntegerField('Identifier',primary_key=True)
    hiragana = models.CharField('Hiragana',max_length=6)
    romanji = models.CharField('Romanji',max_length=6)
    
    def __str__(self):
        return self.hiragana
        
class Katakana(models.Model):
    id = models.IntegerField('Identifier',primary_key=True)
    katakana = models.CharField('Katakana',max_length=6)
    romanji = models.CharField('Romanji',max_length=6)
    
    def __str__(self):
        return self.katakana
        
class Vocabulary(models.Model):
    id = models.IntegerField('Identifier',primary_key=True)
    group = models.CharField('Group',max_length=20)
    vocabulary = models.CharField('Vocabulary',max_length=20)
    pronounciation = models.CharField('Pronounciation',max_length=20,null=True)
    translation = models.CharField('Translation',max_length=20)
    note = models.CharField('Note',max_length=20,null=True)
    
    def __str__(self):
        return self.vocabulary