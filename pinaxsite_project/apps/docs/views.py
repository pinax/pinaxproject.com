import cPickle as pickle
import httplib2
import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json


def documentation_index(request):
    ctx = {
        "versions": [
            ("0.7", "0.7"),
            ("dev", "Development")
        ]
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("docs/index.html", ctx)


def documentation_detail(request, version, slug=None):
    
    # figure out which branch to pull docs from based on version
    try:
        branch = {"0.7": "0.7.X", "dev": "master"}[version]
    except KeyError:
        raise Http404("no version")
    else:
        real_version = {"master": "0.9a2.dev5"}.get(branch, branch)
    
    # when no slug is given we are looking at a version detail so just
    # render a template for it
    if slug is None:
        ctx = {
            "doc": fetch_doc(branch, "index"),
            "version": version,
            "real_version": real_version,
        }
        ctx = RequestContext(request, ctx)
        return render_to_response("docs/%s_index.html" % version, ctx)
    
    # handle old documentation and redirect to new URL
    if slug.endswith(".html"):
        redirect_to = reverse("documentation_detail", kwargs={
            "version": version, "slug": slug.replace(".html", "")
        })
        return HttpResponsePermanentRedirect(redirect_to)
    
    ctx = {
        "doc": fetch_doc(branch, slug),
        "version": version,
        "real_version": real_version,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("docs/detail.html", ctx)


def fetch_doc(branch, slug):
    branch_path = os.path.join(settings.DOCS_ROOT, "output-%s" % branch)
    # check if slug is a directory
    if os.path.isdir(os.path.join(branch_path, slug)):
        doc_file = os.path.join(slug, "index.fpickle")
    else:
        doc_file = "%s.fpickle" % slug
    doc_path = os.path.join(branch_path, doc_file)
    if os.path.exists(doc_path):
        with open(doc_path) as fp:
            parts = pickle.load(fp)
        return parts
    else:
        raise Http404("no doc")
