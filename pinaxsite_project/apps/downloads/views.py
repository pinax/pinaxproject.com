from django.shortcuts import render

from downloads.utils import latest_version


def download_index(request):
    ctx = {
        "latest_dev_version": latest_version("Pinax", "http://dist.pinaxproject.com/dev/"),
    }
    return render(request, "downloads/index.html", ctx)
