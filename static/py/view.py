from tasks.models import Module
from groups.models import Group
from string import ascii_letters, digits
from random import sample
from django.contrib.auth.models import User


def get_user_by_name(name):
    return User.objects.get(username=name)


def get_new_key(length=16):
    all = ascii_letters + digits
    return "".join(sample(all,length))


def is_user_authenticated(request):
    return request.user.is_authenticated


def get_element_by_starts_with(start,request):
    element=list(filter(lambda e:e.startswith(start), request.POST))
    if element: return element[0].split(start)[1]
    else: return False


def get_base_context(request, **kwargs):
    context = {}
    # cookie cleanup
    for c_name, c_value in list(filter(lambda c:c[0].startswith('temp'), request.session.items())):
        if 'keep_cookies' in kwargs and c_name in kwargs['keep_cookies']: continue
        del request.session[c_name]
    for s in request.session.items():print(s)
    # context['all_modules'] = Module.objects.filter(is_public=True, is_active=True)
    #sider context
    if request.user.is_authenticated:
        context['my_modules']    = Module.objects.all()
        context['my_groups']     = Group.objects.all()
        context['new_modules']    = Module.objects.filter(author=request.user)
        # context['my_groups']      = [[group, getattr(group,'moduls').count()] for group in Group.objects.filter(members__id=request.user.id)]
        # context['new_modules']    = Module.objects.filter(author=request.user)
    return context