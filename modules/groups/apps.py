
from __future__ import unicode_literals

from django.apps import AppConfig


class GroupsConfig(AppConfig):
    name = 'modules.groups'

    def ready(self):
        # refresh Cache.
        from models import GroupCodes
        GroupCodes.refresh_cache()
