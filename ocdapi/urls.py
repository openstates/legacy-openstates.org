from django.conf.urls import patterns, include
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   ('^$', RedirectView.as_view(url='http://docs.opencivicdata.org/en/latest/api/index.html')),
   ('', include('boundaries.urls')),
   ('', include('imago.urls')),
   ('', include('locksmith.auth.urls')),
   (r'^admin/', include(admin.site.urls)),
)