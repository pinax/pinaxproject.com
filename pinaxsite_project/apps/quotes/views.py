from django.shortcuts import render_to_response
from django.template import RequestContext

from quotes.models import Quote



def home(request):
    
    quotes = Quotes.objects.all()
    
    ctx = RequestContext(request, {
        "quotes": quotes,
    })
    return render_to_response("quotes/home.html", ctx)
