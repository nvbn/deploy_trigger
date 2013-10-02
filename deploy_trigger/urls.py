from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import IndexPageView


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', IndexPageView.as_view(), name='home'),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
