from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .models import Video


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