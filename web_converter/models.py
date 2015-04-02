import base64
import os

from django.db import models


class Video(models.Model):

	identifier = models.TextField(null=False, blank=True)
	url = models.TextField(null=False, blank=True)
	created = models.DateTimeField(auto_now_add=True, 
		null=False, blank=False)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.identifier = base64.urlsafe_b64encode(
				os.urandom(8)).strip('=')
		super(Video, self).save(*args, **kwargs)