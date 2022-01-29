from django.shortcuts import render, redirect
from static.py.view import get_base_context, is_user_authenticated, get_new_key, get_element_by_starts_with, get_user_by_name
from .models import Group
# errors
from django.db.utils import IntegrityError
from django.http import Http404


def HomeView(request): pass
def InviteView(request): pass

def CreateView(request):
    if not is_user_authenticated(request):
        return redirect("/accounts/register/groups_create/")

    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        return render(request, 'group_create.html', context)

    # scrap data
    name        = request.POST['name']
    description = request.POST['description']
    author      = request.user
        
    # creation
    try: new_group = Group.objects.create(
            name        = name,
            author      = author,
            description = description,
            id          = get_new_key())
    except IntegrityError: pass

    # save
    new_group.save()  
    
    # proceed
    return redirect(f'/groups/{new_group.id}/')
# CreateGroupView - end


def ShowView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404
        
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['group'] = cur_group
        return render(request, 'group_show.html', context)
    
    # what request
    if "btn_mem" in request.POST:
        return redirect(f'/groups/{id}/users/')
    if "btn_edit" in request.POST:
        return redirect(f'/groups/{id}/edit/')
    if "btn_join" in request.POST:
        if request.user not in cur_group.members.all():
            if request.user not in cur_group.members_pending.all():
                cur_group.members_pending.add(request.user)
    if "btn_leave" in request.POST:
        if request.user in cur_group.members.all():
            cur_group.members.remove(request.user)
    if "btn_cancel_join" in request.POST:
        if request.user in cur_group.members_pending.all():
            cur_group.members_pending.remove(request.user)

    # what?
    return redirect(f'/groups/{id}/')
# ShowView - end


def EditView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404

    # is user author 
    if cur_group.author != request.user: raise Http404
        
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['group'] = cur_group
        return render(request, 'group_edit.html', context)
    
    # cancel
    if "cancel_btn" in request.POST:
        return redirect(f'/groups/{id}/')

    # delete module
    if 'btn_del' in request.POST:
        cur_group.delete()
        return redirect(f'/')

    # scrap data
    name            = request.POST['name']
    description     = request.POST['description']

    # save module
    if 'btn_save' in request.POST:
        cur_group.name = name
        cur_group.description = description
        cur_group.save()
        return redirect(f'/groups/{id}/') 
# EditView - end


def MembersView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404

    # is user author 
    if cur_group.author != request.user: raise Http404
        
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['group'] = cur_group
        return render(request, 'group_members.html', context)

    # what request
    mem_add = get_element_by_starts_with("btn_mem_add_",request)
    mem_rem = get_element_by_starts_with("btn_mem_rem_",request)
    mem_del = get_element_by_starts_with("btn_mem_del_",request)

    # add user
    if mem_add:
        mem_add = get_user_by_name(mem_add)
        if mem_add not in cur_group.members_pending.all():
            return Http404
        cur_group.members_pending.remove(mem_add)
        cur_group.members.add(mem_add)
        return redirect(f'/groups/{id}/users/')

    # remove (from pending) user
    if mem_rem:
        mem_rem = get_user_by_name(mem_rem)
        if mem_rem in cur_group.members_pending.all():
            cur_group.members_pending.remove(mem_rem)
        return redirect(f'/groups/{id}/users/')

    # delete (from members) user
    if mem_del:
        mem_del = get_user_by_name(mem_del)
        if mem_del in cur_group.members.all():
            cur_group.members.remove(mem_del)
        return redirect(f'/groups/{id}/users/')
    
    # what
    return redirect(f'/groups/{id}/')
# MembersView - end


def JoinView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404

    # is not user author 
    if cur_group.author == request.user: raise Http404
    
    print(cur_group.members.all())
    if request.user in cur_group.members.all(): raise Http404
    if request.user in cur_group.members_pending.all(): raise Http404

    print("DIE SCUM ("+request.user.username+")")

    cur_group.members_pending.add(request.user)
    cur_group.save()

    return redirect(f'/groups/{id}/') 