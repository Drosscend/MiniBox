from django.shortcuts import render
from WebGraphique.forms.UploadFileForm import UploadFileForm

# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if str(request.FILES['file'])[-4:] == ".csv":
            fileName = form.save()
            return render(request, 'index.html', {'form': form, 'file': str(fileName.file)})
        else :
            return render(request, 'index.html', {'form': form, 'error': "Le fichier doit être un .csv"})
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})