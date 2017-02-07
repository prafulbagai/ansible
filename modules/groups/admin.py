
from django.contrib import admin
from models import Groups, GroupCodes, Category


class CategoryAdmin(admin.ModelAdmin):
    pass


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'date')
    search_fields = ['name']


class GroupCodesAdmin(admin.ModelAdmin):
    list_display = ('name', 'master_name', 'group', 'date',)
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Groups, GroupsAdmin)
admin.site.register(GroupCodes, GroupCodesAdmin)
