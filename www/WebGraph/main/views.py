from django.shortcuts import render
from main.forms.UploadFileForm import UploadFileForm

# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['fichier']
            if file.name.endswith('.csv'):
                csv_reader = file.read()

                csv_reader = csv_reader.decode('utf-8')

                lines = []

                for line in csv_reader.split('\r\n'):
                    lines.append(line.split(","))

                return render(request, 'index.html', {'form': form, 'lines': lines})
            else :
                return render(request, 'index.html', {'form': form, 'error': "Le fichier doit être un .csv"})
        else :
            return render(request, 'index.html', {'form': form, 'error': "Une erreur est survenue"})
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})