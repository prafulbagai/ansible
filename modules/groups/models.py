
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from cache import Cache
from modules.utils import datetime_to_milli


class CountryCodes(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.code + ', ' + self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Groups(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    icon = models.ImageField(upload_to='media/', null=True, blank=True)
    phone_number = models.CharField(max_length=255, default='', null=True, blank=True)
    category = models.ForeignKey(Category, db_index=True)
    date = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.name

    def to_json(self):
        category = self.category
        group_id = self.id
        group_codes = GroupCodes.get_codes(group_id)
        try:
            icon = str(self.icon.url)
        except:
            icon = ''

        return {
            'id': group_id,
            'group_name': self.name,
            'phone_number': self.phone_number,
            'icon': icon,
            'category': category.name,
            'category_id': category.id,
            'date': datetime_to_milli(self.date),
            settings.GROUP_CODES_JSON_KEY: group_codes,
        }


class GroupCodes(models.Model):
    master_name = models.CharField(max_length=255, db_index=True, unique=True)
    group = models.ForeignKey(Groups, db_index=True)
    country_code = models.ForeignKey(CountryCodes, db_index=True, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # saving master_name in uppercase.
        self.master_name = self.master_name.upper()
        super(GroupCodes, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.master_name

    @classmethod
    def get_codes(cls, group_id):
        return list(cls.objects.filter(group_id=group_id) \
                               .values_list('master_name', flat=True) \
                               .distinct())

    @classmethod
    def refresh_cache(cls):
        """Add data to cache."""
        group = {g.name: g.to_json() for g in Groups.objects.all()}
        code_vs_group = {g.master_name.upper(): g.group.name for g in cls.objects.all() \
                                                                         .select_related('group')}

        Cache.flush()
        # Cache GroupVsCode Mapping
        Cache.hmset(settings.GROUP_CODE_REDIS_KEY, code_vs_group)
        # Caching Group Details - appending master name in Group.
        Cache.hmset(settings.GROUP_REDIS_KEY, group)
        return {
            'groups': group,
            'codes': code_vs_group
        }


class UnavailableCodes(models.Model):
    master_name = models.CharField(max_length=255, db_index=True)
    count = models.IntegerField(default=0, db_index=True)

    def __unicode__(self):
        return self.master_name


class UnavailableCodesHistory(models.Model):
    device_id = models.IntegerField(db_index=True)
    master_name = models.CharField(max_length=255, db_index=True)
    date = models.DateTimeField(auto_now=True, db_index=True)
