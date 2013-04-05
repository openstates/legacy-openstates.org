from django.conf.urls.defaults import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
   (r'', include('boundaries.urls')),
   (r'^locust/', include('locust.urls')),
   #(r'^admin/', include(admin.site.urls)),
)
