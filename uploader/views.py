import time, os, json, base64, urllib, hmac, sha

from django.http import HttpResponse

from samba.settings import AWS_SECRET_ACCESS_KEY
from samba.settings import AWS_ACCESS_KEY_ID
from samba.settings import AWS_STORAGE_BUCKET_NAME

def get_signed_s3_url(request):

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