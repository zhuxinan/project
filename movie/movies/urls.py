from django.conf.urls import url
from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logined/(\d+)/$',views.logined,name='logined'),
    url(r'^register/$',views.register,name='register'),
    url(r'^usericted/(\d+)/$',views.collected,name='collected'),
    url(r'^addconfo/(\d+)/$',views.userinfo,name='userinfo'),
    url(r'^collellect/(\d+)/$',views.addcollect,name='addcollect'),
    url(r'^delcollect/(\d+)/$',views.delcollect,name='delcollect'),
    url(r'^edituser/(\d+)/$',views.edituser,name='edituser'),
    url(r'^logout/$',views.logout,name='logout'),
]