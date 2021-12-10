from django.forms import Form, MultiWidget,\
    CharField, TextInput, Textarea


class GroupForm(Form):
    author = CharField(
        label='Автор',
        max_length=64,
        widget=TextInput(attrs={
                'disabled': '',
                'id':       'gru_author',
    }))#name-end
    name = CharField(
        label='Название',
        max_length=64,
        widget=TextInput(attrs={
                'disabled': '',
                'id':       'gru_name',
    }))#name-end
    members = CharField(
        label='Участники',
        max_length=32,
        widget=Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'gru_members',
    }))