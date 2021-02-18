from django import forms
from .models import Module


class ModuleForm(forms.Form):

    name = forms.CharField(
        label='Название',
        max_length=32,
        widget=forms.TextInput(
            attrs={} ) )
    #name-end

    author = forms.CharField(
        label='Автор',
        max_length=32,
        widget=forms.TextInput(
            attrs={
                'disabled': '',
            } ),
        required=False )
    #author-end

    assigned_to = forms.CharField(
        label='ASSIGN',
        max_length=1024,
        widget=forms.Textarea(
            attrs={
                'style': 'resize: none',
            } ) )
    #assigned_to-end

    tasks = forms.CharField(
        label='TASKS',
        max_length=1024,
        widget=forms.Textarea(
            attrs={
                'style': 'resize: none',
            } ) )
    #tasks-end


class AddTaskForm(forms.Form):
    name = forms.CharField(
        label='Название',
        max_length=200,
        widget=forms.TextInput(
            attrs={
            }
        )
    )
    user = forms.CharField(
        label='Пользователь',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'disabled': '',
            }
        ),
        required=False
    )
    content = forms.CharField(
        label='Условие',
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                'style': 'height:500px'
            }
        )
    )
    # module = forms.ChoiceField(
    #     choices=enumerate([m.name for m in Module.objects.all()])
    # )

