
from django.contrib import admin

from forms import GroupCodesForm
from models import Groups, GroupCodes, Category, UnavailableCodes, CountryCodes


@admin.register(CountryCodes)
class CountryCodesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ['name', 'code']


@admin.register(UnavailableCodes)
class UnavailableCodesAdmin(admin.ModelAdmin):
    list_display = ('master_name', 'count')
    search_fields = ['master_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'date', 'phone_number', 'category')
    search_fields = ['name']


@admin.register(GroupCodes)
class GroupCodesAdmin(admin.ModelAdmin):
    form = GroupCodesForm
    list_display = ('master_name', 'group', 'date')
    search_fields = ['master_name', 'group__name']
