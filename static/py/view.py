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



def get_element_by_starts_with(start:str,request) -> str:
    '''
    Returns first element's value, that starts with start
    If got nothing, returns False
    
    example: request.POST is ['sth_526']
        get_elements_by_starts_with('sth_', request) -> '526'
    '''
    elements=list(filter(lambda e:e.startswith(start), request.POST))
    if elements: return elements[0].split(start)[1]
    else: return False


def get_elements_by_starts_with(start:str,request) -> list:
    '''
    Returns all element's value, that starts with start
    If got nothing, returns empty list
    
    example: request.POST is ['sth_526', 'sth_283']
        get_elements_by_starts_with('sth_', request) -> ['526', '283']
    '''
    elements=list(filter(lambda e:e.startswith(start), request.POST))
    if elements: return list(map(lambda x: x.split(start)[1], elements))
    else: return []



def get_base_context(request, page_name='⚠', **kwargs):
    context = {'page_name': page_name}
    # session cleanup
    for c_name, c_value in list(filter(lambda c:c[0].startswith('temp'), request.session.items())):
        if 'keep_cookies' in kwargs and c_name in kwargs['keep_cookies']: continue
        del request.session[c_name]
    # log cookies and session data for debug
    for cookie_name, cookie_value in request.COOKIES.items():print('🍪',cookie_name, '-=-', cookie_value)
    for session in request.session.items():print('🖥️ ',session)
    #sider context MAKE THIS MEET ITS FINAL DOOM
    if request.user.is_authenticated:
        context['my_modules']    = Module.objects.all()
        context['my_groups']     = Group.objects.all()
        context['new_modules']    = Module.objects.filter(author=request.user)
        # context['my_groups']      = [[group, getattr(group,'moduls').count()] for group in Group.objects.filter(members__id=request.user.id)]
        # context['new_modules']    = Module.objects.filter(author=request.user)
    return context