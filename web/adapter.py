from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# class SocialLoginAdapter(DefaultAccountAdapter):

#     def respond_user_inactive(self, request, user):
#         return HttpResponseRedirect(reverse_lazy("common:home_msg")+'?login_message=inactive_user')

class AccountAdapter(DefaultAccountAdapter):

  def get_login_redirect_url(self, request):
      return '/login'