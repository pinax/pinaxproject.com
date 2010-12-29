import httplib2

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
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
    if slug is None:
        ctx = RequestContext(request)
        return render_to_response("docs/%s_index.html" % version, ctx)
    repo = "pinax/pinax"
    if slug.endswith(".html"):
        redirect_to = reverse("documentation_detail", kwargs={
            "version": version, "slug": slug.replace(".html", "")
        })
        return HttpResponseRedirect(redirect_to)
    try:
        branch = {"0.7": "0.7.3", "dev": "master"}[version]
    except KeyError:
        raise Http404("no version")
    else:
        version = {"master": "0.9a2.dev5"}.get(branch, branch)
    h = httplib2.Http()
    # fetch tree SHA for latest commit on master
    url = "http://github.com/api/v2/json/commits/list/%s/%s" % (repo, branch)
    response, content = h.request(url, "GET")
    data = json.loads(content)
    tree_sha = data["commits"][0]["tree"]
    # fetch a list of blobs at the master tree SHA (allowing us to grab docs/)
    url = "http://github.com/api/v2/json/tree/show/%s/%s" % (repo, tree_sha)
    response, content = h.request(url, "GET")
    data = json.loads(content)
    docs_tree_sha = [b["sha"] for b in data["tree"] if b["name"] == "docs"][0]
    # fetch the index documentation
    url = "http://github.com/api/v2/json/tree/full/%s/%s" % (repo, docs_tree_sha)
    response, content = h.request(url, "GET")
    data = json.loads(content)
    for blob in data["tree"]:
        if blob["name"] == "%s.txt" % slug:
            url = "http://github.com/api/v2/json/blob/show/%s/%s" % (repo, blob["sha"])
            response, content = h.request(url, "GET")
            ctx = {
                "doc": {"body": content}
            }
            ctx = RequestContext(request, ctx)
            return render_to_response("docs/detail.html", ctx)
    raise Http404()