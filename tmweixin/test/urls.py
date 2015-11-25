from django.conf.urls import patterns, include, url
import views as v

urlpatterns = patterns('',
                       url(r'^sns_base/', v.sns_base, name='sns_base'),
                       url(r'^sns_user_info/', v.sns_user_info, name='sns_user_info'),
                       url(r'^auth', v.auth, name='auth'),
                       )
