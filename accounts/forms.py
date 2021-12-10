from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'password1',
            'password2')
    def save(self, commit=True):
        user = super(RegisrationForm, self).save(commit=True)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AccountForm(forms.Form):
    username = forms.CharField(
        label='username',
        max_length=64,
        widget=forms.TextInput(attrs={'disabled': ''})
    )#username-end
    status = forms.CharField(
        label='Status',
        max_length=64,
        widget=forms.TextInput()
    )#status-end
    bio = forms.CharField(
        label='Bio',
        max_length=64,
        widget=forms.TextInput()
    )#bio-end