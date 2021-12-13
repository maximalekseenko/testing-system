from tasks.models import Module
from groups.models import Group
from string import ascii_letters, digits
from django.utils.translation import gettext
from random import sample


def get_new_key(length=16):
    all = ascii_letters + digits
    return "".join(sample(all,length))


def is_user_authenticated(request):
    return request.user.is_authenticated


def get_base_context(request, pagename="", buttonname=""):
    context = {}
    #old
    context['pagename']    = pagename
    context['buttonname']  = buttonname
    context['user']        = request.user
    # context['all_modules'] = Module.objects.filter(is_public=True, is_active=True)
    #sider content
    if request.user.is_authenticated:
        context['my_modules']    = Module.objects.all()
        context['my_groups']     = Group.objects.all()
        context['new_modules']    = Module.objects.filter(author=request.user)
        # context['my_groups']      = [[group, getattr(group,'moduls').count()] for group in Group.objects.filter(members__id=request.user.id)]
        # context['new_modules']    = Module.objects.filter(author=request.user)
    #languesge content
    if True:
        #errors
        context['tr_err_name_exist'] = "Имя уже занято"
        #account
        context['tr_registration'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_reg_already'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_register'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_signin'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_not_reg'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_username'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_password1'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_password2'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        #groups
        context['tr_group_creation'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_author'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_group_name'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_description'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_create'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_edit'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_join'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_group'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        #module
        context['tr_module_creation'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_module_name'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_module'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_pass'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_edit_tasks'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        context['tr_add_task'] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"



    return context