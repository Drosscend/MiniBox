from django.shortcuts import render
from WebGraphique.forms.UploadFileForm import UploadFileForm
from WebGraphique.models import CSVFile

# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        fileName = form.save()
        return render(request, 'WebGraphique/index.html', {'form': form, 'file': str(fileName.file)})
    else:
        form = UploadFileForm()
    return render(request, 'WebGraphique/index.html', {'form': form})