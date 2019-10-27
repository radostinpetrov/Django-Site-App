from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from todoapp.views import index
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='home'),
    path('', views.index)
]


