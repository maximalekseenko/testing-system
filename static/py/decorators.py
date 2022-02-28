from django.template.response import TemplateResponse
from django.http import Http404



def check_author(func):
    def _check_author(request, model, *args, **kargs):
        # error if not author
        if model.author != request.user: raise Http404
        # 
        return func(request, model, *args, **kargs)
    return _check_author



def check_object_exist(model_type):
    def _check_object_exist(func):
        def __check_object_exist(request, *args, **kargs):
            # get id
            id = request.GET['id']
            # error if not valid
            try: model = model_type.objects.get(id=id)
            except model_type.DoesNotExist: raise Http404
            # 
            return func(request, model, *args, **kargs)
        return __check_object_exist
    return _check_object_exist



def check_auntification(func):
    def _check_auntification(request, *args, **kargs):
        # auntificate if needed
        if not request.user.is_authenticated:
            return TemplateResponse(request, 'to_sign.html')
        # 
        return func(request, *args, **kargs)
    return _check_auntification