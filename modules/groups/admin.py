
from django.contrib import admin

from models import Groups, GroupCodes, Category, UnavailableCodes


@admin.register(UnavailableCodes)
class UnavailableCodesAdmin(admin.ModelAdmin):
    list_display = ('master_name', 'count')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'date', 'phone_number', 'category')
    search_fields = ['name']


@admin.register(GroupCodes)
class GroupCodesAdmin(admin.ModelAdmin):
    list_display = ('master_name', 'group', 'date')
    search_fields = ['master_name', 'group__name']
