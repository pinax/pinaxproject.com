from django import template

from downloads.models import Release



register = template.Library()



class BaseReleaseNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token, **kwargs):
        bits = token.split_contents()
        
        if len(bits) != 3:
            raise template.TemplateSyntaxError("%r takes exactly two arguments "
                "(first argument must be 'as')" % bits[0])
        if bits[1] != "as":
            raise template.TemplateSyntaxError("Second argument to %r must be "
                "'as'" % bits[0])
        
        return cls(bits[2], **kwargs)


class LatestReleaseNode(BaseReleaseNode):
    
    def __init__(self, context_var, kind):
        self.context_var = context_var
        self.kind = kind
    
    def render(self, context):
        
        if self.kind == "stable":
            queryset = Release.objects.filter(stable=True)
        elif self.kind == "development":
            queryset = Release.objects.filter(stable=False)
        else:
            raise ValueError("Unknown kind in LatestReleaseNode.render")
        
        queryset = queryset.order_by("-timestamp")
        try:
            context[self.context_var] = queryset[0]
        except IndexError:
            context[self.context_var] = None
        
        return u""


class OlderReleasesNode(BaseReleaseNode):
    
    def __init__(self, context_var):
        self.context_var = context_var
    
    def render(self, context):
        
        latest_releases = Release.objects.order_by("-timestamp")[:2]
        context[self.context_var] = Release.objects.exclude(
            id__in = latest_releases
        ).order_by("-timestamp")
        
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
