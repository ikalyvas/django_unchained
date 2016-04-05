from django.conf.urls.defaults import * 
from Weblvn.WeblvnApp import views
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', views.main),
    # url(r'^Weblvn/', include('Weblvn.foo.urls')),
    url(r'^save_on_insert/$', views.save_on_insert),
    url(r'^insert_form/$', views.insert_form),
    url(r'^search-current-lvn/$', views.search_current),
    url(r'^submit/$', views.search_current),
    url(r'^search-lvn/$', views.search_lvn),
    url(r'^search-author-commits/$', views.search_author_commits),
    url(r'^listing/$', views.listing, name='authorslist'),
    url(r'^listing/(?P<page_index>\d+)/$', views.listing, name='authorslist'),
    #url(r'^search/$', views.search),
    url(r'^uniqueLvn/$',views.uniqueLvn),
    url(r'^changedrevision/$',views.changedrevision),
    url(r'^lvnaffectingtable/$',views.lvn_affecting_table),
    url(r'^manage_wiki_entries/$',views.manage_wiki_entries),
    url(r'^feature_related_table/$',views.feature_related_table),
    url(r'^manage_ISU_paths/$',views.isu_path_table),
    url(r'^insert_ISU_path_form/$',views.insert_ISU_path_form),
    url(r'^handle_uploaded_file/$',views.handle_uploaded_file),
    url(r'^delete_uploaded_file/$',views.delete_uploaded_file),
    url(r'^insert_LVN_feature_entry/$',views.insert_and_upload),
    url(r'^fetched_row/$',views.fetch_row),
    url(r'^fetched_range/$',views.fetch_range),
    url(r'^main/$', views.main),
    url(r'^show_build_info/$',views.show_build_info),
    url(r'^do_svndiff/$',views.do_svndiff),
    url(r'^$',views.main),
    url(r'^svnhistory/(?P<revision_>\d+).txt',views.error_detail),
    url(r'^(?P<branch_name>\w+)/(?P<bfr_lvn>\w+)/(?P<author>\w+)/(?P<revision>\d{6})/$',views.prefilled_insert_wiki_form),
    url(r'^manage_KBEntries/$',views.kbentry_table),
    url(r'^insert_KBEntry_form/$',views.insert_KBEntry_form),
    url(r'^buildstable/$',views.builds_table),
    url(r'^manage_build_entries/$',views.manage_build_entries),
     # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^my_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^admin/', include(django.contrib.admin.urls)),
)
