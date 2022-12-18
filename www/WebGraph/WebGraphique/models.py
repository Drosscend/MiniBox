from django.db import models

# Create your models here.
class CSVFile(models.Model):
    file = models.FileField(upload_to='files', blank=False, null=False)