from allauth.account.views import email_verification_sent
from django.urls import include, path, re_path

urlpatterns = [
    path('confirm-email/', email_verification_sent, name='account_email_verification_sent'),
    re_path(r'^', include('rest_auth.urls')),
    re_path(r'^registration/', include('rest_auth.registration.urls')),
]
