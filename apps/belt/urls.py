from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg', views.register),
    url(r'^log', views.login),
    url(r'^dashboard', views.dashboard),
    url(r'^wish_items/create', views.create_item),
    url(r'^add', views.add),
    url(r'^del', views.destroy),
    url(r'^remove', views.remove),
    url(r'^wish_items/(?P<number>\d+)', views.items),
]