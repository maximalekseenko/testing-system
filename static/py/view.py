from django.shortcuts import render, redirect
from tasks.models import Module
from groups.models import Group
from string import ascii_letters, digits, punctuation
from random import sample


def get_new_key(length=16):
    all = ascii_letters + digits
    return "".join(sample(all,length))


def is_user_pure_for_page(request):
    if not request.user.is_authenticated: return False
    return True


def is_user_registred(request):
    if not request.user.is_authenticated: return False
    return True


def is_user_authenticated(request):#fix
    if not request.user.is_authenticated: return False
    return True


def get_base_context(request, pagename="", buttonname=""):
    context = {}
    #old
    context['pagename']    = pagename
    context['buttonname']  = buttonname
    context['user']        = request.user
    context['all_modules'] = Module.objects.filter(is_public=True, is_active=True)
    #sider content
    if request.user.is_authenticated:
        context['my_groups']      = [[group, getattr(group,'moduls').count()] for group in Group.objects.filter(members__id=request.user.id)]
        context['new_modules']    = Module.objects.filter(author=request.user)
    #languesge content
    if True:
        #errors
        context['tr_err_name_exist'] = "Имя уже занято"
        #account
        context['tr_registration'] = "Регистрация"
        context['tr_register'] = "Зарегистрироваться"
        context['tr_signin'] = "Войти"
        context['tr_username'] = "Имя пользователя"
        context['tr_password1'] = "Пароль"
        context['tr_password2'] = "Подтверждение пароля"
        #groups
        context['tr_group_creation'] = "Создание группы"
        context['tr_author'] = "Автор"
        context['tr_group_name'] = "Название группы"
        context['tr_description'] = "Описание"
        context['tr_create'] = "Создать"
        context['tr_edit'] = "Редактировать"
        context['tr_join'] = "Вступить"
        context['tr_group'] = "Группа"
    else:
        context['tr_registration'] = "Registration"
        context['tr_register'] = "Register"
        context['tr_username'] = "Username"
        context['tr_password1'] = "Password"
        context['tr_password2'] = "Password confirmation"



    return context