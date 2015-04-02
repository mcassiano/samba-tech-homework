from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from zencoder import Zencoder

from samba.settings import ZENCODER_API_KEY


class EncoderTestCase(TestCase):

	def test_encoder(self):

		zencoder_client = Zencoder(ZENCODER_API_KEY)
		django_client = Client()

		input_file = "http://dinamica-sambatech.s3.amazonaws.com/sample.dv"

		response = zencoder_client.job.create(input_file)
		zencoder_job_id = response.body['id']

		self.assertEqual(response.code, 201)

		while 1:
			progress = zencoder_client.job.progress(zencoder_job_id)
			state = progress.body['outputs'][0]['state']

			assert (progress.code != 200 or progress.code != 201)

			if state == 'finished':
				break