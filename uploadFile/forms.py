from django import forms

class UploadFileForm(forms.Form):
    document = forms.FileField()