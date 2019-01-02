from __future__ import unicode_literals
from django.db import models
from ML.ExtractFeatures import Extract
from ML.predict import predict

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    #isMalware = models.IntegerField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description