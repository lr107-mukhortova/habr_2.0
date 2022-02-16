from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm
from .models import MyUser, Profile
from django.contrib.auth.hashers import make_password, check_password
from .services import login_req
from django.views.generic.base import TemplateView

from datetime import date, datetime


def registration_user(request):
    context = {'form':RegistrationForm()}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            try:
                MyUser.objects.get(email=email)
                form.add_error(None,'такой чел уже есть')
            except:
                user = MyUser(email=email,
                                username=username,
                                password = make_password(password),
                                created_at = datetime.now(),
                                updated_at = datetime.now())
                
                user.save()
                prof = Profile(to_user = user)
                prof.save()
                request.session['authorized'] = True
                request.session['user_id'] = user.id
                request.session['admin'] = False
                request.session['moderator'] = False
                if not remember:
                    request.session.set_expiry(0)
                return redirect('profile')
    return render(request, 'me/registration.html', context)


class MyLoginView(TemplateView):
    template_name = 'me/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            context ={'form': form}
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                remember = form.cleaned_data['remember']
                try:
                    user = MyUser.objects.get(email=email)
                    if check_password(password, user.password):
                        request.session['authorized'] = True
                        request.session['user_id'] = user.id
                        if user.admin:
                            request.session['admin'] = True
                        else:
                            request.session['admin'] = False
                        if user.moderator:
                            request.session['moderator'] = True
                        else:
                            request.session['moderator'] = False
                        if not remember:
                            request.session.set_expiry(0)
                        
                        return redirect('profile')
                    else:
                        form.add_error(None, 'неверный логин или пароль')
                except:
                    form.add_error(None, 'неверный логин или пароль')
            return render(request, self.template_name, context)


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context ={'form': form}
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            try:
                user = MyUser.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['authorized'] = True
                    request.session['user_id'] = user.id
                    if user.admin:
                        request.session['admin'] = True
                    else:
                        request.session['admin'] = False
                    if user.moderator:
                        request.session['moderator'] = True
                    else:
                        request.session['moderator'] = False
                    if not remember:
                        request.session.set_expiry(0)
                    
                    return redirect('profile')
                else:
                    form.add_error(None, 'неверный логин или пароль')
            except:
                form.add_error(None, 'неверный логин или пароль')
        return render(request, 'me/login.html', context)
    else:
        form = LoginForm()
        context = {'form': form}

        return render(request, 'me/login.html', context)
  

@login_req
def profile(request):
    user = MyUser.objects.get(pk=request.session['user_id'])
    prof = Profile.objects.get(pk=request.session['user_id'])
    context = {'obj':user, 'prof':prof}
    return render(request, 'me/profile.html',context)
    
def logout_us(request):
    del request.session['authorized'] 
    del request.session['user_id']
    request.session['admin'] = False
    request.session['moderator'] = False

    return redirect('main_page')

@login_req
def common_edd(request):

    if request.method == "POST":
        user = get_object_or_404(MyUser, pk=request.session['user_id'])
        try:
            flag = MyUser.objects.get(email=request.POST['email'])
            if flag.email == request.POST['email']:
                flag = None
        except:
            flag = None
        if flag:
            error = 'такой email уже существует'
            context = {'error':error, 'obj':user}
            return render(request, 'me/common_edit.html', context)
        else:
            user.email = request.POST['email']
            user.username = request.POST['username']
            user.updated_at = datetime.now()
            user.save()
            return redirect('profile')
    else:
        user = get_object_or_404(MyUser, pk=request.session['user_id'])
        context = {'obj':user}
        return render(request, 'me/common_edit.html', context)

@login_req
def privat_edd(request):
    if request.method == "POST":
        user = get_object_or_404(MyUser, pk=request.session['user_id'])
        if check_password(request.POST['o_password'], user.password):
            user.password = make_password(request.POST['password'])
            user.updated_at = datetime.now()
            user.save()
            return redirect('profile')
        else:
            context = {'obj':user, 'error':'неверный пароль'}
            return render(request, 'me/private_edit.html', context)
    else:
        user = get_object_or_404(MyUser, pk=request.session['user_id'])
        return render(request, 'me/private_edit.html', {'obj':user})

@login_req
def avatar_edd(request):
    if request.method == "POST":
        user = get_object_or_404(MyUser, pk=request.session['user_id'])
        try:
            data = request.FILES['image']
            if user.avatar.url == '/media/images/profile.jpg' :
                user.avatar = data
            else:
                user.avatar.delete()
                user.avatar = data
        except:
            pass
        user.updated_at = datetime.now()
        user.save()
        return redirect('profile')

    else:
        user = get_object_or_404(MyUser, pk=request.session['user_id'])
        return render(request, 'me/avatar_edit.html', {'obj':user})

def prof_edd(request):
    if request.method == 'POST':
        prof = Profile.objects.get(pk=request.session['user_id'])
        prof.status = request.POST['status']
        prof.save()
        return redirect('profile')
    else:
        prof = Profile.objects.get(pk=request.session['user_id'])
        return render(request, 'me/extra_set_edit.html', {'prof':prof})