
import os
import csv
import zipfile

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from models import ExcelFile, Icons
from modules.utils import upload_to_s3, download_file_from_url
from modules.groups.models import Category, Groups, GroupCodes


@receiver(post_save, sender=ExcelFile)
def save_excel(sender, instance, **kwargs):
    file = download_file_from_url(instance.file.url, 'temp.csv')
    filepath = os.path.join(settings.BASE_DIR, file)
    with open(filepath, 'rU') as f:
        rows = csv.reader(f, delimiter=',', quotechar='"')
        for n, row in enumerate(rows):
            if n == 0:
                continue
            gname, category, codes, phone_number = row
            if not (gname or category or codes):
                continue
            """ Adding to DB. """
            category, created = Category.objects \
                                        .get_or_create(name=category)
            group, gcreated = Groups.objects \
                                    .update_or_create(name=gname,
                                                      category=category,
                                                      defaults={'phone_number': phone_number})
            for code in codes.split(','):
                code, ccreated = GroupCodes.objects \
                                           .update_or_create(master_name=code,
                                                             defaults={'group': group})


@receiver(post_save, sender=Icons)
def save_icons(sender, instance, **kwargs):
    file = download_file_from_url(instance.icons.url, 'temp.zip')
    filepath = os.path.join(settings.BASE_DIR, file)
    targetdir = settings.BASE_DIR
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(targetdir)

    directory = os.path.join(targetdir, settings.ICON_FOLDER_NAME)
    icons = [p for p in os.listdir(directory)]
    for icon in icons:
        if not icon.endswith('.png'):
            continue
        gname = icon.split('.')[0]
        group = Groups.objects.filter(name=gname).first()
        if group:
            filepath = os.path.join(directory, icon)
            upload_to_path = ('/media/' + icon)
            url = upload_to_s3(filepath, upload_to_path)
            group.icon = icon
            group.save()
