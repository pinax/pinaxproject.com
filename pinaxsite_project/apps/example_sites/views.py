from django.shortcuts import render_to_response
from django.template import RequestContext

from example_sites.forms import SiteSubmissionForm



def submit_site(request):
    
    template_name = "example_sites/submit_site.html"
    
    if request.method == "POST":
        form = SiteSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SiteSubmissionForm()
    
    ctx = RequestContext(request, {
        "form": form,
    })
    return render_to_reponse(template_name, ctx)