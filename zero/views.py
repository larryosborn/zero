from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))
