from django.shortcuts import render, redirect
from static.py.view import get_base_context, get_new_key, get_element_by_starts_with, get_user_by_name
from static.py.decorators import check_auntification, check_object_exist, check_author
from .models import Group, ModuleData
from tasks.models import Module
#
from datetime import datetime
from re import split
# errors
from django.db.utils import IntegrityError


def HomeView(request): pass
def InviteView(request): pass



@check_auntification
def CreateView(request):
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        return render(request, 'group_create.html', context)


    # create
    while True:
        try: 
            new_group = Group.objects.create(
                name        = request.POST['name'],
                description = request.POST['description'],
                author      = request.user,
                id          = get_new_key())
            break
        except IntegrityError: continue


    # save
    new_group.save()  
    

    # proceed
    return redirect(f'/groups/?id={new_group.id}')
# CreateGroupView - end



@check_object_exist(Group)
def ShowView(request, cur_group):
    # get mod_count for page
    mod_count = int(request.GET.get('q')) if request.GET.get('q') else 3
        

    # render page
    if request.method != 'POST':
        ## content
        context = get_base_context(request)
        ## mod show on page
        context['mod_count'] = ':' + str(mod_count)
        context['can_mod_load'] = len(cur_group.moduls_data.all()) > mod_count
        ## group
        context['group'] = cur_group
        ## render
        return render(request, 'group_show.html', context)
    
 
    # what request
    ## load more old moduls for preview
    if "btn_mod_load" in request.POST: 
        return redirect(f'/groups/?id={cur_group.id}&q={mod_count+3}')
    ## redirect to moduls editor
    if "btn_edit_mod" in request.POST:
        return redirect(f'/groups/moduls/?id={cur_group.id}')
    ## redirect to members editor
    if "btn_edit_mem" in request.POST:
        return redirect(f'/groups/members/?id={cur_group.id}')
    ## redirect to editor
    if "btn_edit" in request.POST:
        return redirect(f'/groups/edit/?id={cur_group.id}')
    ## join group
    if "btn_join" in request.POST:
        if request.user not in cur_group.members.all() and \
            request.user not in cur_group.members_pending.all() and \
            request.user != cur_group.author:
            cur_group.members_pending.add(request.user)
    ## leave group
    if "btn_leave" in request.POST:
        if request.user in cur_group.members.all():
            cur_group.members.remove(request.user)
    ## cancel join request
    if "btn_cancel_join" in request.POST:
        if request.user in cur_group.members_pending.all():
            cur_group.members_pending.remove(request.user)
    ## pass module
    pass_module_id = get_element_by_starts_with('btn_pass_',request)
    if pass_module_id:
        request.session[f'module_{pass_module_id}_group'] = cur_group.id
        return redirect(f'/tasks/pass/?id={pass_module_id}')


    # reload
    return redirect(request.get_raw_uri())
# ShowView - end



@check_object_exist(Group)
@check_author
def ModulsView(request, cur_group):
    # render page
    if request.method != 'POST':
         # context
        context = get_base_context(request)
        context['group'] = cur_group
         # render
        return render(request, 'group_moduls.html', context)


    # what request
    ## back
    if 'btn_back' in request.POST:
        return redirect(f'/groups/?id={cur_group.id}')
    ## remove module
    rem_mod_id = get_element_by_starts_with("btn_rem_",request)
    if rem_mod_id:
        ModuleData.objects.get(module__id__exact=rem_mod_id).delete()
    ## results of module
    res_mod_id = get_element_by_starts_with("btn_res_",request)
    if res_mod_id:
        return redirect(f'/groups/moduls/results/?id={cur_group.id}&m={res_mod_id}')
    ## change deadline
    deadline = get_element_by_starts_with("deadline_",request)
    if deadline:
        changed = cur_group.moduls_data.get(module__id__exact=deadline)
        changed.deadline = datetime.strptime(request.POST["deadline_"+deadline], '%Y-%m-%dT%H:%M')
        changed.save()
    ## add module
    if 'add_mod' in request.POST:
        for mod_id in split('=|&', request.POST['add_mod_id']):
            ## check id for existance
            try:mod = Module.objects.get(id=mod_id)
            except:continue

            if cur_group.moduls_data.filter(module__exact=mod):
                moduleData = cur_group.moduls_data.get(module__exact=mod)
                moduleData.clean()
                moduleData.deadline = datetime.now()
                moduleData.save()
            else:
                new_ModuleData = ModuleData.objects.create(module = mod, deadline = datetime.now())
                new_ModuleData.save()
                cur_group.moduls_data.add(new_ModuleData)
                cur_group.save()
    

    # reload
    return redirect(request.get_raw_uri())
# ModulsView - end



@check_object_exist(Group)
@check_author
def ModulesResultsView(request, cur_group):
    cur_module_data = cur_group.moduls_data.get(module__id=request.GET['m'])


    # render page
    if request.method != 'POST':
         # context
        context = get_base_context(request)
        context['module_data'] = cur_module_data
         # render
        return render(request, 'group_moduls_results.html', context)


    # what request
    ## back
    if 'btn_back' in request.POST:
        return redirect(f'/groups/moduls/?id={cur_group.id}')
    

    # reload
    return redirect(request.get_raw_uri())
# ModulsView - end



@check_object_exist(Group)
@check_author
def EditView(request, cur_group): 
    # render page
    if request.method != 'POST':
        ## content
        context = get_base_context(request)
        context['group'] = cur_group
        ## render
        return render(request, 'group_edit.html', context)
    

    # what request
    ## cancel
    if "cancel_btn" in request.POST:
        return redirect(f'/groups/?id={cur_group.id}')
    ## delete module
    if 'btn_del' in request.POST:
        cur_group.delete()
        return redirect(f'/')
    ## save module
    if 'btn_save' in request.POST:
        cur_group.name = request.POST['name']
        cur_group.description = request.POST['description']
        cur_group.save()
        return redirect(f'/groups/?id={cur_group.id}')
    

    # reload
    return redirect(request.get_raw_uri())
# EditView - end



@check_object_exist(Group)
@check_author
def MembersView(request, cur_group): 
    # render page
    if request.method != 'POST':
        ## context
        context = get_base_context(request)
        context['group'] = cur_group
        ## render
        return render(request, 'group_members.html', context)

    # what request
    ## back
    if 'btn_back' in request.POST:
        return redirect(f'/groups/?id={cur_group.id}')
    ## add user
    mem_add = get_element_by_starts_with("btn_mem_add_",request)
    if mem_add:
        ### get user
        mem_add = get_user_by_name(mem_add)
        ### raise if user not pending
        if mem_add not in cur_group.members_pending.all(): return
        ### raise if user not pending
        cur_group.members_pending.remove(mem_add)
        cur_group.members.add(mem_add)
    ## remove (from pending) user
    mem_rem = get_element_by_starts_with("btn_mem_rem_",request)
    if mem_rem:
        ### get user
        mem_rem = get_user_by_name(mem_rem)
        ### remove if pending
        if mem_rem in cur_group.members_pending.all():
            cur_group.members_pending.remove(mem_rem)
    ## delete (from members) user
    mem_del = get_element_by_starts_with("btn_mem_del_",request)
    if mem_del:
        ### get user
        mem_del = get_user_by_name(mem_del)
        ### delete if in group
        if mem_del in cur_group.members.all():
            cur_group.members.remove(mem_del)


    # reload
    return redirect(request.get_raw_uri())
# MembersView - end


@check_auntification
@check_object_exist(Group)
def JoinView(request, cur_group):
    # validation 
    if cur_group.author == request.user: return
    if request.user in cur_group.members.all(): return
    if request.user in cur_group.members_pending.all(): return

    # add user to pending list
    cur_group.members_pending.add(request.user)
    cur_group.save()

    # return 
    return redirect(f'/groups/{id}/') 