
import json

from django.db.models import F
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from difflib import get_close_matches

from cache import Cache
from modules.utils import get_post_params
from models import GroupCodes, Groups, UnavailableCodes


@method_decorator(csrf_exempt, name='dispatch')
class GroupsView(View):

    def get(self, request, *args, **kwargs):
        exists, groups = Cache.get_key(key_type=settings.GROUP_REDIS_KEY)
        if groups:
            groups = {k: v for k, v in groups.iteritems()}
        else:
            groups = {g.name: g.to_json() for g in Groups.objects.all()}

        response = {
            'status': 200,
            'groups': groups
        }
        return JsonResponse(response, safe=False)

    def post(self, request, *args, **kwargs):
        received_codes = get_post_params(request).get('group_codes', [])
        exists, data = Cache.get_key(settings.GROUP_CODE_REDIS_KEY)
        if not exists:  # if not in Cache, fetch from DB and refresh Cache.
            all_codes = set(GroupCodes.objects.all().values_list('master_name',
                                                                 flat=True))
            GroupCodes.refresh_cache()
        else:
            all_codes = data.keys()

        if not all_codes:  # if DB empty, return null.
            response = {
                'status': 200,
                'groups': []
            }
            return JsonResponse(response, safe=False)

        groups, lst = [], []
        for code in received_codes:
            code = code.lower()
            exists, group = Cache.get_key(settings.GROUP_CODE_REDIS_KEY,
                                          code)
            if not exists:
                closest_code = get_close_matches(word=code, cutoff=0.8,
                                                 n=1, possibilities=all_codes)
                if closest_code:
                    code = closest_code[0]
                    exists, group = Cache.get_key(settings.GROUP_CODE_REDIS_KEY,
                                                  code)
                else:
                    group = ''

                uc, created = UnavailableCodes.objects.get_or_create(master_name=code,
                                                                     group=group,
                                                                     defaults={'count': 1})
                if not created:
                    uc.count = F('count') + 1
                    uc.save()

                continue

            if group in lst:
                continue

            exists, gd = Cache.get_key(settings.GROUP_REDIS_KEY, group)
            groups.append(gd)
            lst.append(group)

            # add in DB & Cache.
            if not exists:
                gid, gname = gd['id'], gd['name']
                # inserting in DB.
                GroupCodes.objects.create(master_name=code, group__id=gid)
                # Cache CodeVsGroup Mapping
                Cache.set_key(key=code, value=gname,
                              key_type=settings.GROUP_CODE_REDIS_KEY)
                # Caching Group Details - appending master name in Group.
                Cache.set_key(key=gname, value=code,
                              key_type=settings.GROUP_REDIS_KEY,
                              dict_key=settings.GROUP_CODES_JSON_KEY)

        response = {
            'status': 200,
            'groups': groups
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GroupDetails(View):

    def post(self, request, *args, **kwargs):
        received_groups = get_post_params(request).get('groups', [])
        groups = []
        for group in received_groups:
            exists, details = Cache.get_key(settings.GROUP_REDIS_KEY, group)
            if not exists:  # if not in Cache, fetch from DB and refresh Cache.
                g = Groups.objects.filter(name=group).first()
                if not g:
                    continue
                details = g.to_json()
                GroupCodes.refresh_cache()
            groups.append(details)

        response = {
            'status': 200,
            'groups': groups
        }

        return JsonResponse(response, safe=False)
