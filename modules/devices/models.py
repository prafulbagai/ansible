
from django.db import models
# from modules.consumer.config import PHONE_TYPE_CHOICE
# from modules.consumer.core.models import Timezone, Urls


class OperatingSystem(models.Model):
    """.."""

    android_version = models.CharField(
        max_length=255, db_column="android_version", null=True)
    vendor_os_version = models.CharField(
        max_length=255, db_column="vendor_os_version", null=True)
    vendor_name = models.CharField(
        max_length=100, db_column="vendor_name", null=True)

    class Meta:
        """.."""

        unique_together = (("android_version", "vendor_name"),)
        db_table = 'operating_system'


class DevicesModels(models.Model):
    """.."""

    model = models.CharField(max_length=255, db_column="model")
    board_name = models.CharField(
        max_length=100, db_column="board_name", null=True)
    ram_size = models.FloatField(db_column="ram_size", null=True)
    is_dual_sim = models.BooleanField(db_column="is_dual_sim", default=False)
    internal_space = models.FloatField(
        db_column="internal_space", null=True)
    is_hd = models.BooleanField(db_column="is_hd", default=False)
    phone_type = models.IntegerField(db_column='phone_type')
    screen_width = models.PositiveSmallIntegerField(
        db_column="screen_width", null=True)
    screen_height = models.PositiveSmallIntegerField(
        db_column="screen_height", null=True)
    xdpi = models.FloatField(db_column='xdpi', null=True)
    ydpi = models.FloatField(db_column='ydpi', null=True)
    manufacturer = models.CharField(max_length=255, null=False, db_column='manufacturer')

    class Meta:
        """.."""

        db_table = 'devices_models'
        unique_together = (("model", "manufacturer"),)


class DevicesRegistered(models.Model):
    """.."""

    device_model_id = models.ForeignKey(
        DevicesModels, db_column="device_model_id", null=True)
    imei_1 = models.BigIntegerField(db_column="imei_1", default=0)
    imei_2 = models.BigIntegerField(db_column="imei_2", null=True)
    android_id = models.CharField(
        max_length=50, db_column="android_id", null=True)
    registered_on = models.BigIntegerField(
        db_column="registered_on")
    gaid = models.CharField(max_length=255, db_column='gaid', null=True)
    locale = models.CharField(max_length=255, db_column='locale', null=True)
    sim_country = models.CharField(
        max_length=255, db_column='sim_country', null=True)
    network_country = models.CharField(
        max_length=255, db_column='network_country', null=True)
    gms_version = models.CharField(max_length=255, db_column='gms_version', null=True)
    accounts = models.CharField(max_length=255, db_column='accounts', null=True)
    timezone_id = models.ForeignKey(
        'Timezone', db_column='timezone_id', null=True)

    os_id = models.ManyToManyField(
        OperatingSystem, db_column="os_id", blank=True)
    urls = models.ManyToManyField('Urls', db_column='urls', blank=True, through='DeviceUrls', related_name='devices_urls')

    class Meta:
        """.."""

        unique_together = (('imei_1', 'android_id'),)
        db_table = 'devices_registered'
