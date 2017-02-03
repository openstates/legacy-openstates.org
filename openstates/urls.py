from django.conf.urls import patterns, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # flat pages
    (r'^about/$', TemplateView.as_view(template_name='flat/about.html')),
    (r'^funding/$', TemplateView.as_view(template_name='flat/funding.html')),
    (r'^methodology/$', TemplateView.as_view(template_name='flat/methodology.html')),
    (r'^contributing/$', TemplateView.as_view(template_name='flat/contributing.html')),
    (r'^contact/$', TemplateView.as_view(template_name='flat/contact.html')),
    (r'^categorization/$', TemplateView.as_view(template_name='flat/categorization.html')),
    (r'^csv_downloads/$', TemplateView.as_view(template_name='flat/csv_downloads.html')),
    (r'^reportcard/$', TemplateView.as_view(template_name='flat/reportcard.html')),
    (r'^tos/$', TemplateView.as_view(template_name='flat/tos.html')),
    (r'^map_svg/$', TemplateView.as_view(template_name='flat/openstatesmap.svg')),

    # api docs
    (r'^api/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/', permanent=True)),
    (r'^api/metadata/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/metadata.html', permanent=True)),
    (r'^api/bills/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/bills.html', permanent=True)),
    (r'^api/committees/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/committees.html', permanent=True)),
    (r'^api/legislators/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/legislators.html', permanent=True)),
    (r'^api/events/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/events.html', permanent=True)),
    (r'^api/districts/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/districts.html', permanent=True)),

    (r'^api/', include('billy.web.api.urls')),
    (r'^admin/', include('billy.web.admin.urls')),
    (r'^djadmin/', include(admin.site.urls)),
    (r'^', include('billy.web.public.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT,
          'show_indexes': True}))
