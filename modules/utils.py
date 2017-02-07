
import json
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)


def get_post_params(request):
    data = request.POST
    if not data:
        try:
            data = json.loads(request.body)
        except:
            data = {}
    return data


def datetime_to_milli(dt):
    dt = dt.replace(tzinfo=None)
    return int((dt - epoch).total_seconds() * 1000)
