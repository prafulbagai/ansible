
from __future__ import unicode_literals

from django.apps import AppConfig


class DataConfig(AppConfig):
    name = 'modules.data'

    def ready(self):
        import modules.data.signals
