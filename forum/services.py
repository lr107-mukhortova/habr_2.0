from .models import Post
from me.models import MyUser
from django.shortcuts import redirect

def user_req(func):
    def wrapper(request, post_id, **kargs):
        if Post.objects.get(pk=post_id).user.id == request.session.get('user_id', None) or request.session['admin'] or request.session['moderator']:
            return func(request, post_id, **kargs)
        return redirect('main_page')
    return wrapper

def admin_req(func):
    def wrapper(request, *args, **kargs):
        if MyUser.objects.get(pk=request.session['user_id']).admin:
            return func(request, *args, **kargs)
        return redirect('main_page')
    return wrapper

def moderator_req(func):
    def wrapper(request, *args, **kargs):
        a = MyUser.objects.get(pk=request.session['user_id'])
        if a.moderator or a.admin:
            return func(request, *args, **kargs)
        return redirect('main_page')
    return wrapper


def tags_search(model, list_of_tags):
    flag = True
    for tag in list_of_tags:
        if tag not in model.short_description:
            flag = False
            break
    return flag
