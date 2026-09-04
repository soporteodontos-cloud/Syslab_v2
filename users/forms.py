from django import forms

from users.models import CustomUsers, MY_AREAS


class CustomUsersCreateModelForm(forms.ModelForm):
    class Meta:
        model = CustomUsers
        fields = {'id', 'username', 'password', 'first_name', 'last_name', 'email'}
        widgets = {
            'password': forms.PasswordInput()
        }
    field_order = ['username', 'password', 'first_name', 'last_name', 'email']


class CustomUsersUpdateModelForm(forms.ModelForm):
    class Meta:
        model = CustomUsers
        fields = {'id', 'username', 'first_name', 'last_name', 'email'}
    field_order = ['username','first_name', 'last_name', 'email']


class CustomUsersAreasModelForm(forms.ModelForm):
    areas = forms.MultipleChoiceField(choices=MY_AREAS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomUsers
        fields = {'id', 'areas'}


class CustomUsersPasswordResetModelForm(forms.ModelForm):
    class Meta:
        model = CustomUsers
        fields = {'id', 'password'}
        widgets = {
            'password': forms.PasswordInput()
        }
    field_order = ['password']
