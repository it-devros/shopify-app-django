import shopify

from devApp import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from .decorators import anonymous_required
from main_app.models import AuthShop
from django.db.models import Q
import pdb

def get_return_address(request):
  return request.GET.get(auth.REDIRECT_FIELD_NAME) or resolve_url(settings.LOGIN_REDIRECT_URL)


# @anonymous_required
def login(request, *args, **kwargs):
  # The `shop` parameter may be passed either directly in query parameters, or
  # as a result of submitting the login form.
  shop = request.POST.get('shop', request.GET.get('shop'))
  print('++++++++++++++++++++ it is login ++++++++++++++++++')
  # If the shop parameter has already been provided, attempt to authenticate immediately.
  if shop:
    print('++++++++++++++++ authenticate +++++++++++++++++')
    return authenticate(request, *args, **kwargs)

  return render(request, "shopify_auth/login.html", {
    'SHOPIFY_APP_NAME': settings.SHOPIFY_APP_NAME
  })


#@anonymous_required
def authenticate(request, *args, **kwargs):
  shop = request.POST.get('shop')

  if shop:
    from shopify_auth import views as shopify_auth_views
    redirect_uri = request.build_absolute_uri(reverse(shopify_auth_views.finalize))
    #redirect_uri = request.build_absolute_uri(reverse(shopify_auth.views.finalize))
    scope = settings.SHOPIFY_APP_API_SCOPE
    print(redirect_uri)
    redirect_uri = redirect_uri[:-1]
    temp_url = shopify.Session(shop.strip()).create_permission_url(scope, redirect_uri)

    permission_url = temp_url
    
    if settings.SHOPIFY_APP_IS_EMBEDDED:
      # Embedded Apps should use a Javascript redirect.
      return render(request, "shopify_auth/iframe_redirect.html", {
        'redirect_uri': permission_url
      })
    else:
      # Non-Embedded Apps should use a standard redirect.
      return HttpResponseRedirect(permission_url)
  else:
    shop = request.GET.get('shop')
    if shop:
      return finalize(request, *args, **kwargs)

  return_address = get_return_address(request)

  return HttpResponseRedirect(return_address)


#@anonymous_required
def finalize(request, *args, **kwargs):
  shop = request.GET.get('shop')
  shopify_session = {}
  try:
    current_shops = []
    current_shops = AuthShop.objects.filter(Q(shop_name=shop) | Q(token=kwargs.get('token'))).order_by('-id')
    if not current_shops:
      print('++++++++++++++++++ creating shop and access token ++++++++++++++++++')
      shopify_session = shopify.Session(shop, token=kwargs.get('token'))
      shopify_session.request_token(request.GET)
      print(shopify_session.url)
      current_shop = AuthShop(shop_name=shopify_session.url, token=shopify_session.token)
      current_shop.save()
    else:
      print('++++++++++++++++++ reloading shop and access token ++++++++++++++++++')
      print(current_shops[0].shop_name)
      shopify_session = shopify.Session(current_shops[0].shop_name, token=current_shops[0].token)
  except:
    print('++++++++++++++++++ authentication error ++++++++++++++++++')
    login_url = reverse('shopify_auth.views.login')
    return HttpResponseRedirect(login_url)

  # Attempt to authenticate the user and log them in.
  user = auth.authenticate(myshopify_domain=shopify_session.url, token=shopify_session.token)
  if user:
    auth.login(request, user)

  return_address = get_return_address(request)
  return HttpResponseRedirect(return_address)
