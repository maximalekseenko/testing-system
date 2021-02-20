from django import forms
from .models import Module


class ModuleForm(forms.Form):

    name = forms.CharField(
        label='Название',
        max_length=64,
        widget=forms.TextInput(attrs={
                'disabled': '',
                'id':       'name',
    }))#name-end
    author = forms.CharField(
        label='Автор',
        max_length=64,
        widget=forms.TextInput(attrs={
                'disabled': '',
                'id':       'author',
    }))#name-end
    tasks = forms.CharField(
        label='Участники',
        max_length=32,
        widget=forms.Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'tasks',
    }))#tasks-end
    assigned_to = forms.CharField(
        label='Участники',
        max_length=32,
        widget=forms.Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'assigned_to',
    }))#assigned_to-end
    creation_date = forms.CharField(
        label='Название',
        max_length=64,
        widget=forms.TextInput(attrs={
                'disabled': '',
                'id':       'date',
    }))#name-end
    #bool
    is_active           = models.BooleanField(default=True)
    is_public           = models.BooleanField(default=False)

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

