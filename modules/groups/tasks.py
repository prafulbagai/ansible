
from django.db.models import F

from c26_mclients import app
from modules.devices.models import DevicesRegistered
from models import GroupCodes, UnavailableCodesHistory, UnavailableCodes


@app.task()
def add_to_unavailable(data):
    imei_1, imei_2 = data['IMEI1'], data['IMEI2']
    android_id, gaid = data['android_id'], data['GAID']
    device_id = DevicesRegistered.get_device_id(imei_1=imei_1, imei_2=imei_2,
                                                gaid=gaid, android_id=android_id)

    codes = data['codes']
    available_codes = GroupCodes.objects.filter(master_name__in=codes) \
                                        .values_list('master_name', flat=True)
    user_unavailable_codes = UnavailableCodesHistory.objects \
                                                    .filter(device_id=device_id,
                                                            master_name__in=codes) \
                                                    .values_list('master_name',
                                                                 flat=True)
    refreshed = False
    for code in codes:
        if code in available_codes:
            # refresh cache.
            if not refreshed:  # refresh only once.
                GroupCodes.refresh_cache()
                refreshed = True
            continue
        if code in user_unavailable_codes:
            continue

        # save as history
        UnavailableCodesHistory.objects.create(device_id=device_id,
                                               master_name=code)
        # increase the count by +1
        uc, created = UnavailableCodes.objects.get_or_create(master_name=code,
                                                             defaults={'count': 1})
        if not created:
            uc.count = F('count') + 1
            uc.save()
