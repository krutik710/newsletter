from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Subscription(models.Model):
	email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
	is_active = models.IntegerField(default=0)
	subkey = models.CharField(max_length=100)
	unsubkey = models.CharField(max_length=100)

	def __str__(self):
		return str(self.email)


class Newsletter(models.Model):
	subject = models.CharField(max_length=1000)
	body = models.TextField(blank=True)
	html = RichTextField(config_name='content')

	def __str__(self):
		return self.subject