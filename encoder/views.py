import json

from django.http import HttpResponse

from zencoder import Zencoder

from samba.settings import ZENCODER_API_KEY


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