from django import forms


class GroupForm(forms.Form):

    name = forms.CharField(
        label='Название',
        max_length=64,
        widget=forms.TextInput(attrs={
                'disabled': '',
                'id':       'mem_name',
    }))#name-end
    author = forms.CharField(
        label='Автор',
        max_length=64,
        widget=forms.TextInput(attrs={
                'disabled': '',
                'id':       'mem_author',
    }))#name-end
    members = forms.CharField(
        label='Участники',
        max_length=32,
        widget=forms.Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'mem_members',
        } ) )