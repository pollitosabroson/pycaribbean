# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views
from books.views import BookViewSet, AuthorViewSet
from rest_framework.routers import DefaultRouter
admin.autodiscover()


router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet, base_name='book')
router.register(r'author', AuthorViewSet)

if getattr(settings, 'ALLOW_SERVE_STATIC_FILES', False):
    urlpatterns = static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.*', views.AngularAppView.as_view(), name='app')
)
