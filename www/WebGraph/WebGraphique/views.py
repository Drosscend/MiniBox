from django.shortcuts import render
from WebGraphique.forms.UploadFileForm import UploadFileForm
from WebGraphique.models import CSVFile
from WebGraph.settings import BASE_DIR
import csv
import os

# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if str(request.FILES['file'])[-4:] == ".csv":


            # Suppression des anciens CSV
            allCSV = CSVFile.objects.all()
            for aCSV in allCSV:
                os.remove(str(BASE_DIR) + "\\" + str(aCSV.file))
                aCSV.delete()

            # Enregistrement du nouveau
            fileName = form.save()

            # Récupération des lines du fichier
            f = open( str(BASE_DIR) + "\\" + str(fileName.file))
            lines = list(csv.reader(f))
            f.close()

            return render(request, 'index.html', {'form': form, 'file': str(fileName.file), 'lines' : lines})
        else :
            return render(request, 'index.html', {'form': form, 'error': "Le fichier doit être un .csv"})
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})