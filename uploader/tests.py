from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
import json

class UploaderTestCase(TestCase):

	def test_get_signed_s3_url(self):

		client = Client()
		response = client.get(reverse('get_signed_s3_url'))

		self.assertEqual(response.status_code, 400)

		response = client.get(reverse('get_signed_s3_url'), {
			's3_object_name': 'sample.dv',
			's3_object_type': 'application/octet-stream'
			})

		self.assertEqual(response.status_code, 200)