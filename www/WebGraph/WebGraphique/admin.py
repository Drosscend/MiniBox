from django.contrib import admin
from WebGraphique.models import CSVFile
# Register your models here.
model_list = [CSVFile]
admin.site.register(model_list)