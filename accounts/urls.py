from django.conf.urls import patterns,url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html' }, name='login_url') ,
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logged_out.html'}, name='logout_url'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change.html', 'post_change_redirect': settings.HOME}, name='password_change_url'),
    url(r'^forgot_password/', 'django.contrib.auth.views.password_reset',{'template_name':'accounts/password_reset_form.html','email':'accounts/password_reset_email.html'},name="forgot_password_url"),
)

urlpatterns += patterns('accounts.views',
    url(r'^register/','register',name="register_url"),
)
