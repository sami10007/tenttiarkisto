from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'exams.views.frontpage'),
    # url(r'^tenttiarkisto/', include('tenttiarkisto.foo.urls')),
    url(r'^courses/$', 'exams.views.courselist'),
    url(r'^courses/add/$', 'exams.views.addcourse'),
    url(r'^courses/(?P<course_id>\d+)/(.+)?$', 'exams.views.courseview'),
    url(r'^exams/(?P<exam_id>\d+)/(.+)?$', 'exams.views.examview'),
    url(r'^exams/add/$', 'exams.views.addexam'),

    # account stuff
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', 'exams.views.register'),
    url(r'^account/$', 'exams.views.modifyaccount'),
    url(r'^ownexams/$', 'exams.views.accountexams'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# serve uploaded files in dev
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

