from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from djnago.conf.urls import url
from . import views
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #url(r'^result/',),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    url(r'^$', views.button),
    url(r'^result', views.external),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 
    


