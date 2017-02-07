
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from cache import Cache
from modules.utils import datetime_to_milli


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Groups(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    icon = models.ImageField(upload_to='', null=True, blank=True)
    phone_number = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, db_index=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def to_json(self):
        category = self.category
        group_id = self.id
        group_codes = GroupCodes.get_codes(group_id)
        try:
            icon = self.icon.url
        except:
            icon = ''

        return {
            'id': group_id,
            'group_name': self.name,
            'phone_number': self.phone_number,
            'icon': icon,
            'category': category.name,
            'category_id': category.id,
            'group_codes': group_codes,
            'date': datetime_to_milli(self.date),
        }


class GroupCodes(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    master_name = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey(Groups, db_index=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_codes(cls, group_id):
        return cls.objects.filter(group_id=group_id).values_list('master_name',
                                                                 flat=True) \
                                                    .distinct()

    @classmethod
    def refresh_cache(cls):
        """Add data to cache."""
        group = {g.name: g.to_json() for g in Groups.objects.all()}
        code_vs_group = {g.master_name.lower(): g.group.name for g in cls.objects.all() \
                                                                         .select_related('group')}

        # Cache GroupVsCode Mapping
        Cache.hmset(settings.GROUP_CODE_REDIS_KEY, code_vs_group)
        # Caching Group Details - appending master name in Group.
        Cache.hmset(settings.GROUP_REDIS_KEY, group)
