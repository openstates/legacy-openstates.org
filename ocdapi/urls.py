from django.conf.urls.defaults import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
   ('', include('boundaries.urls')),
   ('', include('locust.urls')),
   ('', include('imago.urls')),
   #(r'^admin/', include(admin.site.urls)),
)
