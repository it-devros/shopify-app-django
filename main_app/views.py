from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils.crypto import get_random_string
from models import AuthAppShopUser, AuthShop, Times, TextConf
from devApp import settings
from shopify_webhook.decorators import webhook
import shopify
import json


@csrf_exempt
@webhook
def uninstall_webhook_callback(request):
	print '++++++++++++++++++ deleting webhook ++++++++++++++++++'
	webhook_data = request.webhook_data
	print webhook_data['domain']
	print request.webhook_domain
	try:
		user = AuthAppShopUser.objects.filter(myshopify_domain=request.webhook_domain).order_by('-id')[0]
		user.delete()
	except:
		pass
	try:
		current_shop = AuthShop.objects.filter(shop_name=request.webhook_domain).order_by('-id')[0]
		current_shop.delete()
	except:
		pass
	print('webhook ok')
	return HttpResponse('ok')


@login_required
def home(request, *args, **kwargs):
	shop_name = request.user.myshopify_domain
	print '++++++++++++++++++ activating webhook ++++++++++++++++++'
	webhook_shop_address = settings.DEV_DOMAIN + '/app/uninstall_webhook_callback/'
	with request.user.session:
		webhook_status = 0
		webhook_shops = shopify.Webhook.find()
		if webhook_shops:
			for webhook_shop in webhook_shops:
				if webhook_shop.address == webhook_shop_address:
					webhook_status = 1
		if webhook_status == 0:
			print '++++++++++++++++++ saving webhook ++++++++++++++++++'
			webhook_shop = shopify.Webhook()
			webhook_shop.topic = 'app/uninstalled'
			webhook_shop.address = webhook_shop_address
			webhook_shop.format = 'json'
			webhook_shop.save()
			
		url = settings.DEV_DOMAIN + settings.STATIC_URL + 'script/script.js'    
		shopify.ScriptTag(dict(event='onload', src=url)).save()


	items = Times.objects.filter(shop_name=shop_name).order_by('-id')
	item = {};
	if items:
		item = items[0]

	conf_items = TextConf.objects.filter(shop_name=shop_name).order_by('-id')
	conf_item = {};
	if conf_items:
		conf_item = conf_items[0]


	return render(request, "main_app/home.html", { "item": item, "conf": conf_item })


@login_required
def help(request, *args, **kwargs):
	return render(request, "main_app/help.html", {})

@csrf_exempt
def setTime(request, *args, **kwargs):
	shop_name = request.user.myshopify_domain

	days = request.GET.get("days")
	hours = request.GET.get("hours")
	mins = request.GET.get("mins")
	secs = request.GET.get("secs")

	items = Times.objects.filter(shop_name=shop_name).order_by('-id')
	if items:
		item = items[0]
		item.days = days
		item.hours = hours
		item.mins = mins
		item.secs = secs
		item.save()
	else:
		item = Times(shop_name=shop_name, days=days, hours=hours, mins=mins, secs=secs)
		item.save()

	return HttpResponse("ok")


@csrf_exempt
def saveConf(request, *args, **kwargs):
	shop_name = request.user.myshopify_domain

	content = request.GET.get("content")
	font_color = request.GET.get("font_color")
	font_weight = request.GET.get("font_weight")
	font_size = request.GET.get("font_size")

	items = TextConf.objects.filter(shop_name=shop_name).order_by('-id')
	if items:
		item = items[0]
		item.content = content
		item.font_color = font_color
		item.font_weight = font_weight
		item.font_size = font_size
		item.save()
	else:
		item = TextConf(shop_name=shop_name, content=content, font_color=font_color, font_weight=font_weight, font_size=font_size)
		item.save()

	return HttpResponse("ok")



@csrf_exempt
def get_settings(request, *args, **kwargs):

	print('++++++++++++++ getting settigns ++++++++++++++++++')

	shop_name = request.GET.get('shop')
	callback = request.GET.get('callback')
	uid = request.GET.get('uid')
	
	items = Times.objects.filter(shop_name=shop_name)
	conf_items = TextConf.objects.filter(shop_name=shop_name)

	response_string = ''
	if items:
		json_str = ""
		item = items[0]
		if conf_items:
			conf_item = conf_items[0]
			json_dic = { 'days':item.days, 'hours':item.hours, 'mins':item.mins, 'secs': item.secs, 'content': conf_item.content, 'font_color': conf_item.font_color, 'font_weight': conf_item.font_weight, 'font_size': conf_item.font_size }
			json_str = json.dumps(json_dic)
		else:
			json_dic = { 'days':item.days, 'hours':item.hours, 'mins':item.mins, 'secs': item.secs, 'content': "", 'font_color': "", 'font_weight': "", 'font_size': "" }
			json_str = json.dumps(json_dic)
		response_string = 'window["' + callback + '"](' + json_str + ');'

	return HttpResponse(response_string, content_type='text/javascript')


