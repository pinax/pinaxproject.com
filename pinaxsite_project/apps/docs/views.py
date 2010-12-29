import cPickle as pickle
import httplib2

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json


def documentation_index(request):
    ctx = {
        "versions": ["0.7", "dev"]
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("docs/index.html", ctx)


def documentation_detail(request, version, slug=None):
    # when no slug is given we are looking at a version detail so just
    # render a template for it
    if slug is None:
        ctx = RequestContext(request)
        return render_to_response("docs/%s_index.html" % version, ctx)
    
    # handle old documentation and redirect to new URL
    if slug.endswith(".html"):
        redirect_to = reverse("documentation_detail", kwargs={
            "version": version, "slug": slug.replace(".html", "")
        })
        return HttpResponsePermanentRedirect(redirect_to)
    
    # figure out which branch to pull docs from based on version
    try:
        branch = {"0.7": "0.7.X", "dev": "master"}[version]
    except KeyError:
        raise Http404("no version")
    else:
        version = {"master": "0.9a2.dev5"}.get(branch, branch)
    
    with open("/home/anduin/pinax-docs/output-%s/%s.fpickle" % (branch, slug)) as fp:
        parts = pickle.load(fp)
    ctx = {
        "doc": parts,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("docs/detail.html", ctx)
