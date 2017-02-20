
from django.http import JsonResponse
from django.views.generic import View

from modules.groups.models import GroupCodes


class CacheRefresh(View):

    def get(self, request, *args, **kwargs):
        GroupCodes.refresh_cache()
        response = {
            'status': 200,
            'message': 'Success'
        }
        return JsonResponse(response, safe=False)
