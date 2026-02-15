from django import forms


class UploadFileForm(forms.Form):
    #variable name need to be compatible to html name form
    file = forms.FileField(label="file")

