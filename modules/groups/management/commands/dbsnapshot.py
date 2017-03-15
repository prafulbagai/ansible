
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from modules.utils import upload_to_s3


class Command(BaseCommand):
    help = 'DB Snapshot'

    def handle(self, *args, **options):

        file_name = 'DB_' + str(datetime.now().date()) + '.sql'
        file_path = settings.BASE_DIR + '/' + file_name

        command = 'mysqldump -uroot -p17576cube message_groups > ' + file_path
        os.system(command)

        delcommand = 'rm ' + file_path

        if not os.stat(file_path).st_size > 100:
            self.stdout.write(self.style.ERROR('Snapshot UNSUCCESSFULL'))
            os.system(delcommand)
            return

        print upload_to_s3(file_path, file_name)

        os.system(delcommand)

        self.stdout.write(self.style.SUCCESS('Snapshot SUCCESSFULL'))
