
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from difflib import get_close_matches

from cache import Cache
from models import GroupCodes, Groups
from modules.utils import get_post_params


@method_decorator(csrf_exempt, name='dispatch')
class GroupsView(View):

    def post(self, request, *args, **kwargs):
        received_codes = get_post_params(request).get('group_codes', [])
        received_codes = ['IM-BMSOTP1', 'IM-BMSOTP']
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
            master_name = code.split('-')[-1]
            exists, group = Cache.get_key(settings.GROUP_CODE_REDIS_KEY,
                                          master_name)
            if not exists:
                closest_code = get_close_matches(word=master_name, cutoff=0.8,
                                                 n=1, possibilities=all_codes)
                if not closest_code:
                    continue

                master_name = closest_code[0]
                exists, group = Cache.get_key(settings.GROUP_CODE_REDIS_KEY,
                                              master_name)
            if group in lst:
                continue

            exists, gd = Cache.get_key(settings.GROUP_REDIS_KEY, group)
            groups.append(gd)
            lst.append(group)

            # add in DB & Cache.
            if not exists:
                gid, gname = gd['id'], gd['name']
                # inserting in DB.
                GroupCodes.objects.create(name=code, master_name=master_name,
                                          group__id=gid)
                # Cache GroupVsCode Mapping
                Cache.set_key(key=master_name, value=gname,
                              key_type=settings.GROUP_CODE_REDIS_KEY)
                # Caching Group Details - appending master name in Group.
                Cache.set_key(key=gname, value=master_name,
                              key_type=settings.GROUP_REDIS_KEY, append=True)

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
