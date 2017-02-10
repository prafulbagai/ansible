
from django.contrib import admin

from models import ExcelFile, Icons


@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    pass


@admin.register(Icons)
class IconsAdmin(admin.ModelAdmin):
    pass
