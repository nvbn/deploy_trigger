from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import IndexPageView, LogoutView
from .api import router


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', IndexPageView.as_view(), name='home'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
