from django.urls import path ,re_path

from me.views import profile, registration_user, login_user, logout_us,\
     login_req, common_edd, privat_edd, avatar_edd, prof_edd, MyLoginView

urlpatterns = [
    path('', profile, name='profile'),
    path('reg', registration_user, name='registration'),
    path('log', MyLoginView.as_view(), name='login'),
    re_path(r'^logout/*', logout_us, name='logout'),
    path('com_edit', common_edd, name='common_edit'),
    path('priv_edit', privat_edd, name='privat_edit'),
    path('avatar_edd', avatar_edd, name='avatar_edit'),
    path('prof_edit', prof_edd, name='prof_edit')
]