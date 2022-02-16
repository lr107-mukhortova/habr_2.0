from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>', views.current_post, name='current_post'),
    path('', views.main_page, name='main_page'),
    path('make_post', views.make_post, name='make_post'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('my_posts/<int:post_id>', views.my_post, name='my_post'),
    path('post_edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('post_del/<int:post_id>', views.del_post, name='del_post'),
    path('search', views.search, name='search'),
    path('add_comment/<int:post_id>', views.add_comment, name='add_comment'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('admin_panel/user_per_change/<int:user_id>', views.user_permission_change, name='user_per_change'),
    path('admin_post_del/<int:post_id>', views.admin_post_del, name='admin_post_del'),
    path('admin_comment_del/<int:comment_id>', views.comment_del, name='admin_comment_del'),
    path('admin_post_edit/<int:post_id>', views.admin_edit_post, name='admin_post_edit'),
    path('admin_user_change/<int:user_id>', views.admin_user_change, name='admin_user_change')
]