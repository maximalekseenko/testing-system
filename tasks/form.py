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
    }))#author-end

    tasks = forms.CharField(
        label='Задачи',
        max_length=32,
        widget=forms.Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'tasks',
    }))#tasks-end

    assigned_to = forms.CharField(
        label='Группы',
        max_length=32,
        widget=forms.Textarea(attrs={
                'disabled': '',
                'style':    'resize: none; height: 150px;',
                'id':       'assigned_to',
    }))#assigned_to-end
    
    tasks_value = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(attrs={
                'id':'tasks_value',
    }))#tasks_value-end

    assigned_to_value = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(attrs={
                'id':'assigned_to_value',
    }))#assigned_to_value-end

    is_active = forms.BooleanField(
        label='Активен',
        widget=forms.CheckboxInput(attrs={
                'disabled': '',
                'id':       'is_active',
        }), required=False,initial=True
    )#is_active-end

    is_public = forms.BooleanField(
        label='Публичен',
        widget=forms.CheckboxInput(attrs={
                'disabled': '',
                'id':       'is_public',
        }), required=False,initial=True
    )#name-end
