
from django import forms
from models import Groups


class GroupCodesForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Groups.objects.order_by('name'))
