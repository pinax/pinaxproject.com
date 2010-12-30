from django import template

from downloads.models import Release

from pinaxsite_project.utils import AsNode



register = template.Library()



class LatestReleaseNode(AsNode):
    
    def __init__(self, context_var, kind):
        self.context_var = context_var
        self.kind = kind
    
    def render(self, context):
        
        if self.kind == "stable":
            context[self.context_var] = Release.latest_stable()
        elif self.kind == "development":
            context[self.context_var] = Release.latest_development()
        else:
            raise ValueError("Unknown kind in LatestReleaseNode.render")
        
        return u""


class OlderReleasesNode(AsNode):
    
    def render(self, context):
        latest_releases = []
        latest_stable = Release.latest_stable()
        latest_dev = Release.latest_development()
        
        if latest_stable:
            latest_releases.append(latest_stable.id)
        if latest_dev:
            latest_releases.append(latest_dev.id)
        
        older_releases = Release.objects.filter(
            stable=True
        ).exclude(id__in=latest_releases)
        context[self.context_var] = older_releases
        
        return u""


@register.tag
def latest_stable_release(parser, token):
    return LatestReleaseNode.handle_token(parser, token, kind="stable")


@register.tag
def latest_development_release(parser, token):
    return LatestReleaseNode.handle_token(parser, token, kind="development")


@register.tag
def older_releases(parser, token):
    return OlderReleasesNode.handle_token(parser, token)
