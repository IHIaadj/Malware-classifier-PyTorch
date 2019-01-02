from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Document
from ML.ExtractFeatures import Extract
from ML.predict import predict
import sys 

from rest_framework import viewsets
from .serializer import DocumentSerializer 

class DocumentViewset(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

def post(self, request, format = None):
        serializer = DocumentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



def handleFile(request, f): 
    vector = Extract(f)
    return vector


def upload_file(request):
   saved = False
   
   if request.method == "POST":
      #Get the posted form
      form = UploadFileForm(request.POST, request.FILES)
      
      if form.is_valid():
         profile = Document()
         profile.document = form.cleaned_data["document"]
         
         saved = True
         vector = handleFile(request, profile.document)
         prediction = predict(vector)
         #profile.isMalware = 2
         if prediction == 1 :
             test = "MALWARE"
             #profile.isMalware = 1
         else :
             test = "LEGITIME"
             #profile.isMalware = 0

         profile.save()
         return render(request, 'uploadFile/uploaded.html', { 'document' : test })
   else:
      form = UploadFileForm()
		
   return render(request, 'uploadFile/index.html', locals())