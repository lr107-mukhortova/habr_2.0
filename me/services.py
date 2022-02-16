from django.shortcuts import redirect

def login_req(func):
    def wrapper(request, *args, **kargs):
        if request.session.get('authorized', None):
            return func(request, *args, **kargs)
        return redirect('login')
    return wrapper