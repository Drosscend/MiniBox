from django.forms import ModelForm
from WebGraphique.models import CSVFile

class UploadFileForm(ModelForm):
    class Meta:
        model = CSVFile
        fields = ['file']