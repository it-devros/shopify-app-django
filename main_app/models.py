from shopify_auth.models import AbstractShopUser
from django.db import models

# the shop user model for authentication and management of store.

class AuthAppShopUser(AbstractShopUser):
	pass

class AuthShop(models.Model):
	shop_name = models.CharField(max_length=255, unique=True, editable=False)
	shop_id = models.CharField(max_length=255, unique=True, editable=False)
	token = models.CharField(max_length=32, editable=False, default='00000000000000000000000000000000')
	
	def __unicode__(self):
		return "%s" % self.shop_name


class Times(models.Model):
	shop_name = models.CharField(max_length=255, unique=True, editable=False)
	days = models.CharField(max_length=255)
	hours = models.CharField(max_length=255)
	mins = models.CharField(max_length=255)
	secs = models.CharField(max_length=255)

	def __unicode__(self):
		return "%s" % self.shop_name

class TextConf(models.Model):
	shop_name = models.CharField(max_length=255, unique=True, editable=False)
	content = models.CharField(max_length=255)
	font_color = models.CharField(max_length=255)
	font_weight = models.CharField(max_length=255)
	font_size = models.CharField(max_length=255)

	def __unicode__(self):
		return "%s" % self.shop_name

