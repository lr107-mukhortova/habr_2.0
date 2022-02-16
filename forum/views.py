from django.shortcuts import redirect, render
from django.http import HttpResponse
from me.services import login_req
from .services import user_req, tags_search, admin_req, moderator_req
from django.contrib.auth.hashers import make_password
from me.models import MyUser, Profile
from .forms import PostForm
from .models import Comment, Post, Tag
from django.db import connection


from datetime import date, datetime


# Create your views here.


def posts(request):

    abjs = Post.objects.all()
    abjs = sorted(abjs, key=lambda x:x.created_at, reverse=True)
    tags = Tag.objects.all()
    context = {'objs':abjs, 'tags':tags}
    return render(request, 'forum/all_posts.html', context)

def current_post(request, post_id):

    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(to_post=post_id)
    context = {'post':post, 'comments':comments}
    return render(request, 'forum/about_post.html', context)

def main_page(request):
    return render(request, 'forum/main_page.html')

@login_req
def make_post(request):
    if request.method == 'POST':
        user = MyUser.objects.get(pk=request.session['user_id'])
        form = PostForm(request.POST)
        if form.is_valid():
            post :Post = Post(created_at = datetime.now(),
                              updated_at = datetime.now(),
                              model_name = form.cleaned_data['model_name'],
                              short_description = form.cleaned_data['short_description'],
                              full_description = form.cleaned_data['full_description'],\
                              ref_on_git = form.cleaned_data['ref_on_git'],
                              user = user)

            post.save()
            for tag in request.POST.getlist('tags'):
                Tag.objects.get(name=tag).to_post.add(post)
            return redirect('my_posts')
        else:
            tags = Tag.objects.all()
            context = {'form':form, 'tags':tags}
            return render(request, 'forum/make_post.html',context)
    else:
        form = PostForm()
        tags = Tag.objects.all()
        context = {'form':form, 'tags':tags}
        return render(request, 'forum/make_post.html',context)

@login_req
def my_posts(request):
    context = {}
    user = MyUser.objects.get(pk=request.session['user_id'])
    m_posts = Post.objects.filter(user=request.session['user_id'])

    context['posts'] = m_posts 
    return render(request, 'forum/my_posts.html', context)

@login_req
@user_req
def my_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(to_post=post_id)
    context = {'post':post, 'comments':comments}
    return render(request, 'forum/post.html', context)

@login_req
@user_req
def edit_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        form = PostForm(request.POST)
        if form.is_valid():
            post.model_name = form.cleaned_data['model_name']
            post.short_description = form.cleaned_data['short_description']
            post.full_description = form.cleaned_data['full_description']
            post.ref_on_git = form.cleaned_data['ref_on_git']
            post.updated_at = datetime.now()
            post.save()
            return redirect('edit_post', post_id=post_id)
    else:
     
        post = Post.objects.get(pk=post_id)
  
        form = PostForm(instance=post)
        context = {'form':form, 'post':post}
   
        return render(request, 'forum/edit_post.html', context)

@moderator_req
def admin_edit_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        form = PostForm(request.POST)
        if form.is_valid():
            post.model_name = form.cleaned_data['model_name']
            post.short_description = form.cleaned_data['short_description']
            post.full_description = form.cleaned_data['full_description']
            post.ref_on_git = form.cleaned_data['ref_on_git']
            post.updated_at = datetime.now()
            post.save()
            return redirect('admin_post_edit', post_id=post_id)
    else:
     
        post = Post.objects.get(pk=post_id)
        form = PostForm(instance=post)
        context = {'form':form, 'post':post}
   
        return render(request, 'forum/admin_post_edit.html', context)

@login_req
@user_req
def del_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('my_posts')



def search(request):
    if request.method == 'POST':
        context = dict()
        name = request.POST['model_name']
        key_words = request.POST['key_words'].split(' ')
        if key_words == '':
            objects = Post.objects.raw(f"SELECT * FROM forum_post WHERE model_name LIKE '%{name}%'")
            context['objs'] = objects
        elif name == '':
            objects = Post.objects.all()
            lst = []
            for post in objects:
                if tags_search(post, key_words):
                    lst.append(post)
            context['objs'] = lst
        else:
            objects = Post.objects.raw(f"SELECT * FROM forum_post WHERE model_name LIKE '%{name}%'")
            objects_t = Post.objects.all()
            lst = []
            for post in objects_t:
                if tags_search(post, key_words):
                    lst.append(post)
            fin_lst = []
            for post in objects:
                for post_t in objects_t:
                    if post.id == post_t.id:
                        fin_lst.append(post)
            context['objs'] = fin_lst
        if len(request.POST.getlist('tags')):
            lst = request.POST.getlist('tags')
            fin_lst_2 = []
            for post in context['objs']:
                per = post.tag_set.all()
                flag = True
                for tag in per:
                    if tag.name not in lst:
                        flag = False
                if flag:
                    fin_lst_2.append(post)
            context['objs'] = fin_lst_2
        context['tags'] = Tag.objects.all()
        return render(request, 'forum/all_posts.html', context)
    else:
        return redirect('main_page')

@login_req
def add_comment(request, post_id):
    if request.method == 'POST':
        comment = Comment(created_at = datetime.now(),
                          updated_at = datetime.now(),
                          body = request.POST['comment'],
                          to_post = Post.objects.get(pk=post_id),
                          from_user = MyUser.objects.get(pk=request.session['user_id']))
        comment.save()

        return HttpResponse('Коментарий был отправлен')
    else:
        return redirect('main_page')

@admin_req
def admin_panel(request):
    if request.method == 'POST':
        users = MyUser.objects.raw(f"SELECT * FROM me_myuser WHERE email LIKE '%{request.POST['user_name']}%'")
        return render(request, 'forum/admin_panel.html', {'users':users})
    else:

        users = MyUser.objects.all()
        return render(request, 'forum/admin_panel.html', {'users':users})

@admin_req
def user_permission_change(request, user_id):
    if request.method == 'POST':
        
        user = MyUser.objects.get(pk=user_id)
        with connection.cursor() as cursor:
            if request.POST['admin'] != 'Админ':
                cursor.execute(f"UPDATE me_myuser SET admin = {request.POST['admin']} WHERE id = %s",[user_id])
            if request.POST['moderator'] != 'Модератор':
                cursor.execute(f"UPDATE me_myuser SET moderator = {request.POST['moderator']} WHERE id = %s",[user_id])
        return redirect('admin_panel')
    else:
        user = MyUser.objects.get(pk=user_id)
        return render(request, 'forum/permission_change.html', {'user':user})

@moderator_req
def comment_del(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    per = comment.to_post.id
    comment.delete()
    return redirect(f'/posts/{per}')

@moderator_req
def admin_post_del(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('/posts/')

def admin_user_change(request, user_id):
    
    if request.method == 'POST':
        user = MyUser.objects.get(pk=user_id)
        context = {'obj':user}
        try:
            flag = MyUser.objects.get(email=request.POST['email'])
            if flag.email == request.POST['email']:
                flag = None
        except:
            flag = None
        if flag:
            error = 'такой email уже существует'
            context['error'] = error
            return render(request, 'forum/admin_user_chenge.html', context)
        else:
            data = request.FILES.get('files', None)
            if data:
                if user.avatar.url == '/media/images/profile.jpg' :
                    user.avatar = data
                else:
                    user.avatar.delete()
                    user.avatar = data
            prof = Profile.objects.get(pk=user_id)
            prof.status = request.POST['status']
            user.password = make_password(request.POST['password'])
            user.email = request.POST['email']
            user.username = request.POST['username']
            user.updated_at = datetime.now()
            prof.save()
            user.save()
            return redirect('admin_user_change', user_id=user_id)

    else:
        user = MyUser.objects.get(pk=user_id)
        prof = Profile.objects.get(pk=user_id)
        context = {'obj':user,'prof':prof}
        return render(request, 'forum/admin_user_change.html', context)