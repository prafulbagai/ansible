
import zipfile
filepath = '/Users/praful/Desktop/cube/c26_mclients/temp.csv'

targetdir = settings.BASE_DIR
with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(targetdir)

icons = [p for p in os.listdir(targetdir)]
for icon in icons:
    print icon
    gname = icon.split('.')[0]
    group = Groups.objects.filter(name=gname).first()
    if group:
        group.icon = upload_to_s3(file, icon)
        group.save()