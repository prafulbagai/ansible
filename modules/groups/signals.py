
# from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from models import GroupCodes, Groups, UnavailableCodes
# from cache import Cache


@receiver(post_save, sender=Groups)
def update_group_cache(sender, instance, **kwargs):
    GroupCodes.refresh_cache()

    # created = kwargs.get('created')
    # # Cache Groups Mapping
    # if created:  # If new group created, add to cache.
    #     Cache.set_key(key_type=settings.GROUP_REDIS_KEY, key=instance.name,
    #                   value=instance.to_json())
    # else:  # update all the groups again.
    #     Cache.del_key(key_type=settings.GROUP_REDIS_KEY)
    #     group = {g.name: g.to_json() for g in Groups.objects.all()}
    #     Cache.hmset(settings.GROUP_REDIS_KEY, group)


@receiver(post_save, sender=GroupCodes)
def update_code_cache(sender, instance, **kwargs):
    master_name = instance.master_name.upper()

    # Removing code from unavailable code.
    UnavailableCodes.objects.filter(master_name=master_name).delete()

    # Finally Refreshing cache.
    GroupCodes.refresh_cache()

    # group, master_name = instance.group, instance.master_name.lower()

    # created = kwargs.get('created')
    # # Cache Groups Mapping
    # if created:  # If new code created, then append.
    #     Cache.set_key(key=group.name, value=master_name,
    #                   key_type=settings.GROUP_REDIS_KEY,
    #                   dict_key=settings.GROUP_CODES_JSON_KEY)
    # else:  # update the whole group again.
    #     exists, groups = Cache.get_key(settings.GROUP_REDIS_KEY)
    #     if not exists:
    #         data = GroupCodes.refresh_cache()
    #         groups = data.get('groups')
    #         if not groups:
    #             groups = {}

    #     groups.update({group.name: group.to_json()})
    #     Cache.hmset(settings.GROUP_REDIS_KEY, groups)

    # # Cache CodeVsGroup Mapping
    # Cache.set_key(master_name, group.name, settings.GROUP_CODE_REDIS_KEY)
