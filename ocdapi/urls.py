from django.conf.urls import patterns, include
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   ('', include('boundaries.urls')),
   ('', include('imago.urls')),
   (r'^admin/', include(admin.site.urls)),
)
