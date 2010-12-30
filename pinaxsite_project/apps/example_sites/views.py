from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib import messages

from example_sites.forms import SiteSubmissionForm
from example_sites.models import Site



def home(request):
    
    sites = Site.objects.filter(approved=True).order_by("-when_approved")
    
    ctx = RequestContext(request, {
        "sites": sites,
    })
    return render_to_response("example_sites/home.html", ctx)



def submit_site(request):
    
    template_name = "example_sites/submit_site.html"
    
    if request.method == "POST":
        form = SiteSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your submission. It will be reviewed shortly.")
            return redirect("sites_home")
    else:
        form = SiteSubmissionForm()
    
    ctx = RequestContext(request, {
        "form": form,
    })
    return render_to_response(template_name, ctx)