import time, os, json, base64, urllib, hmac, sha

from django.views.generic import FormView
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from samba.settings import ZENCODER_API_KEY
from samba.settings import AWS_SECRET_ACCESS_KEY
from samba.settings import AWS_ACCESS_KEY_ID
from samba.settings import AWS_STORAGE_BUCKET_NAME

from zencoder import Zencoder

from .models import Video

def add_job(request):

    client = Zencoder(ZENCODER_API_KEY)

    s3_input_file = request.POST.get('s3_input_file')
    response = client.job.create(s3_input_file)

    json_response = json.dumps(response.body)

    return HttpResponse(json_response)

def get_status_on_job(request):

    client = Zencoder(ZENCODER_API_KEY)
    zencoder_job_id = request.POST.get('zencoder_job_id')

    response = client.job.progress(zencoder_job_id)
    json_response = json.dumps(response.body)

    return HttpResponse(json_response)


def sign_s3(request):

    AWS_ACCESS_KEY = AWS_ACCESS_KEY_ID
    AWS_SECRET_KEY = AWS_SECRET_ACCESS_KEY
    S3_BUCKET = AWS_STORAGE_BUCKET_NAME

    object_name = request.GET.get('s3_object_name')
    mime_type = request.GET.get('s3_object_type')

    # don't give user full control over filename - avoid ability to overwrite files
    random = base64.urlsafe_b64encode(os.urandom(2))
 
    expires = int(time.time()+300) # PUT request to S3 must start within X seconds
    amz_headers = "x-amz-acl:public-read" # set the public read permission on the uploaded file
    resource = '%s/%s' % (S3_BUCKET, object_name)

    str_to_sign = "PUT\n\n{mime_type}\n{expires}\n{amz_headers}\n/{resource}".format(
        mime_type=mime_type,
        expires=expires,
        amz_headers=amz_headers,
        resource=resource
    )

    sig = urllib.quote_plus(base64.encodestring(hmac.new(AWS_SECRET_KEY, str_to_sign, sha).digest()).strip())
 
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    return HttpResponse(json.dumps({
        'signed_request': '{url}?AWSAccessKeyId={access_key}&Expires={expires}&Signature={sig}'.format(
            url=url,
            access_key=AWS_ACCESS_KEY,
            expires=expires,
            sig=sig
        ),
        'url': url
    }))


def upload_view(request):

    template_name = 'web_converter/index.html'
    return render_to_response(template_name)

def video_detail(request, identifier):

    template_name = 'web_converter/detail.html'
    video = Video.objects.get(identifier=identifier)

    context = {
        'video': video
    }

    return render_to_response(template_name, context)

def save_video_details(request):

    video_url = request.POST.get("video_url")

    video = Video()
    video.url = video_url

    video.save()

    return HttpResponse(reverse('video_detail', 
        kwargs={'identifier': video.identifier}))