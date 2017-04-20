from django.conf.urls import include, url
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from simplekeys.views import RegistrationView, ConfirmationView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    # flat pages
    url(r'^about/$', TemplateView.as_view(template_name='flat/about.html')),
    url(r'^funding/$', TemplateView.as_view(template_name='flat/funding.html')),
    url(r'^methodology/$', TemplateView.as_view(template_name='flat/methodology.html')),
    url(r'^contributing/$', TemplateView.as_view(template_name='flat/contributing.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='flat/contact.html')),
    url(r'^categorization/$', TemplateView.as_view(template_name='flat/categorization.html')),
    url(r'^csv_downloads/$', TemplateView.as_view(template_name='flat/csv_downloads.html')),
    url(r'^reportcard/$', TemplateView.as_view(template_name='flat/reportcard.html')),
    url(r'^tos/$', TemplateView.as_view(template_name='flat/tos.html')),
    url(r'^map_svg/$', TemplateView.as_view(template_name='flat/openstatesmap.svg')),

    # api docs
    url(r'^api/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/', permanent=True)),
    url(r'^api/metadata/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/metadata.html', permanent=True)),
    url(r'^api/bills/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/bills.html', permanent=True)),
    url(r'^api/committees/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/committees.html', permanent=True)),
    url(r'^api/legislators/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/legislators.html', permanent=True)),
    url(r'^api/events/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/events.html', permanent=True)),
    url(r'^api/districts/$', RedirectView.as_view(url='http://docs.openstates.org/en/latest/api/districts.html', permanent=True)),

    url(r'^api/register/$', RegistrationView.as_view(
        confirmation_url='/api/confirm/',
        email_subject='Open States API Key Registration',
    )),
    url(r'^api/confirm/$', ConfirmationView.as_view()),

    url(r'^api/', include('billy.web.api.urls')),
    url(r'^admin/', include('billy.web.admin.urls')),
    url(r'^djadmin/', include(admin.site.urls)),
    url(r'^', include('billy.web.public.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT,
          'show_indexes': True})
    ]
