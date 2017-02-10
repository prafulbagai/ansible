
from __future__ import unicode_literals

from django.db import models


class ExcelFile(models.Model):
    file = models.FileField(upload_to='static/')


class Icons(models.Model):
    icons = models.FileField(upload_to='static/')
