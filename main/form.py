from django import forms


class GroupForm(forms.Form):

    name = forms.CharField(
        label='Название',
        max_length=64,
        widget=forms.TextInput())
    #name-end

    members = forms.CharField(
        label='Автор',
        max_length=32,
        widget=forms.Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'mem_textarea',
        } ) )