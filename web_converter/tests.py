import json

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from .models import Video

class WebConverterTestCase(TestCase):

	def test_save_video(self):

		client = Client()
		response = client.post(reverse('save_video_details'))

		self.assertEqual(response.status_code, 400)

		video_url_test = 'http://test_url.com/video1222'

		response = client.post(reverse('save_video_details'), {
			'video_url': video_url_test
		})

		video_identifier = response.content.strip('/')
		video = Video.objects.get(identifier=video_identifier)

		self.assertEqual(video.identifier, video_identifier)