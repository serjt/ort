"""diplomka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include

from diplomka import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r'^submit/', 'simpleapp.views.submit'),
    url(r'^sign_in/', 'simpleapp.views.sign_in'),
    url(r'^$', 'simpleapp.views.home'),
    url(r'^auth/', 'simpleapp.views.login'),
    url(r'^logout/', 'simpleapp.views.logout'),
    url(r'^add/', 'simpleapp.views.add'),
    url(r'^add_abiturient/', 'simpleapp.views.add_abiturient'),
    # url(r'^edit_abiturient/(\d+)/', 'simpleapp.views.edit_abiturient'),
    url(r'^tour/(\d+)/', 'simpleapp.views.card'),
    url(r'^result/(\d+)/', 'simpleapp.views.tour'),
    url(r'^rating/(\d+)/', 'simpleapp.views.rating'),
    url(r'^tour/$', 'simpleapp.views.all_tables'),
    # url(r'^edit/(\d+)/', 'simpleapp.views.edit'),
    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
