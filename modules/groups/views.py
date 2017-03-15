
import ast

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from cache import Cache
from tasks import add_to_unavailable
from modules.utils import get_post_params, milli_to_datetime, check_args
from models import GroupCodes, Groups


@method_decorator(csrf_exempt, name='dispatch')
class GroupsView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        exists, groups = Cache.get_key(key_type=settings.GROUP_REDIS_KEY)
        if groups:
            for k, v in groups.iteritems():
                try:
                    groups[k] = ast.literal_eval(v)
                except:
                    continue
        else:
            groups = {g.name: g.to_json() for g in Groups.objects.all()}

        response = {
            'status': 200,
            'groups': groups
        }
        return JsonResponse(response, safe=False)

    @check_args('group_codes', 'GAID', 'IMEI1', 'IMEI2', 'android_id')
    def post(self, request, *args, **kwargs):
        rdata = get_post_params(request).get
        received_codes = rdata('group_codes', [])

        exists, data = Cache.get_key(settings.GROUP_CODE_REDIS_KEY)
        if not exists:  # if not in Cache, fetch from DB and refresh Cache.
            GroupCodes.refresh_cache()
            exists, data = Cache.get_key(settings.GROUP_CODE_REDIS_KEY)
            if not exists:
                response = {
                    'status': 400,
                    'error': 'Cache Down.'
                }
                return JsonResponse(response, safe=False)

        all_codes = data.keys()
        if not all_codes:  # if DB empty, return null.
            response = {
                'status': 200,
                'groups': []
            }
            return JsonResponse(response, safe=False)

        groups, lst, unavailable = [], [], []
        for code in received_codes:
            code = code.lower()
            exists, group = Cache.get_key(settings.GROUP_CODE_REDIS_KEY,
                                          code)
            if not exists:  # store in Unavailable codes.
                unavailable.append(code)
                continue

            if group in lst:
                continue

            exists, gd = Cache.get_key(settings.GROUP_REDIS_KEY, group)
            if not exists:
                continue

            groups.append(gd)
            lst.append(group)

        if unavailable:
            data = {
                'codes': unavailable,
                'IMEI1': rdata('IMEI1'),
                'IMEI2': rdata('IMEI2'),
                'GAID': rdata('GAID'),
                'android_id': rdata('android_id')
            }
            add_to_unavailable.delay(data)

        response = {
            'status': 200,
            'groups': groups
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GroupDetails(View):

    @check_args('groups', 'last_synced_time')
    def post(self, request, *args, **kwargs):
        data = get_post_params(request).get
        try:
            last_synced_time = int(data('last_synced_time'))
            dt = milli_to_datetime(last_synced_time)
        except:
            response = {
                'status': 400,
                'error': 'Incorrect time'
            }
            return JsonResponse(response, safe=False)

        received_groups = data('groups', [])

        groups = []

        grp = Groups.objects.filter(name__iin=received_groups, date__gte=dt)
        for group in grp:
            exists, details = Cache.get_key(settings.GROUP_REDIS_KEY, group)
            if not exists:  # if not in Cache, fetch from DB and refresh Cache.
                details = group.to_json()
                GroupCodes.refresh_cache()
            groups.append(details)

        response = {
            'status': 200,
            'groups': groups
        }

        return JsonResponse(response, safe=False)
