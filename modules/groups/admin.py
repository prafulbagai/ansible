
from django import forms
from django.contrib import admin
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

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

    actions = ['add_unavailable_codes_to_group_codes']

    class GroupCodesForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        group = forms.ModelChoiceField(queryset=Groups.objects.order_by('name'),
                                       label='')

    def add_unavailable_codes_to_group_codes(self, request, queryset):
        form = None

        if 'cancel' in request.POST:
            self.message_user(request, 'The request has been Cancelled.')
            return

        if 'apply' in request.POST:
            form = self.GroupCodesForm(request.POST)

            if form.is_valid():
                group = form.cleaned_data['group']
                count = 0
                for code in queryset:
                    count += 1
                    GroupCodes.objects.create(master_name=code.master_name,
                                              group=group)
                    code.delete()

                self.message_user(request, "Successfully added %d code(s) to group '%s'." % (count, group))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.GroupCodesForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        ctx = {'codes': queryset, 'group_form': form}
        return render_to_response('admin/add_unavailable_to_group.html', ctx, RequestContext(request))

    add_unavailable_codes_to_group_codes.short_description = 'Add selected unavailable codes'


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
