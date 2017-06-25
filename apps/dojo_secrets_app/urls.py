from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #login
    url(r'^login$', views.login, name='login'),
    #register
    url(r'^register$', views.register, name='register'),
    #logout
    url(r'^logout$', views.logout, name='logout'),
    #success, welcome page
    url(r'^success$', views.success, name='success'),
    #like secrets
    url(r'^like/(?P<secret_id>\d+)/(?P<location>\d+)$', views.like, name='like'),
    #show most popular secrets
    url(r'^popular$', views.popular, name='popular'),
    #post secrets
    url(r'^postSecret$', views.postSecret, name='postSecret'),
    #delete secrets
    url(r'^delete/(?P<secret_id>\d+)/(?P<location>\d+)$', views.delete, name='delete'),
]