from django import template

from example_sites.models import Site

from pinaxsite_project.utils import AsNode



register = template.Library()



class FeaturedSiteNode(AsNode):
    
    def render(self, context):
        try:
            site = Site.objects.filter(approved=True).get(featured=True)
        except Site.DoesNotExist:
            site = None
        context[self.context_var] = site
        return u""


@register.tag
def featured_site(parser, token):
    return FeaturedSiteNode.handle_token(parser, token)


class RandomSitesNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token, **kwargs):
        bits = token.split_contents()
        
        if len(bits) != 4:
            raise template.TemplateSyntaxError("%r takes exactly three "
                "arguments (first argument must be 'as')" % bits[0])
        if bits[2] != "as":
            raise template.TemplateSyntaxError("Second argument to %r must be "
                "'as'" % bits[0])
        
        return cls(bits[1], bits[3], **kwargs)
    
    def __init__(self, limit, context_var, **kwargs):
        self.limit = template.Variable(limit)
        self.context_var = context_var
    
    def render(self, context):
        limit = self.resolve(context)
        sites = Site.objects.exclude(featured=True).order_by("?")[:limit]
        context[self.context_var] = sites
        return u""


@register.tag
def random_sites(parser, token):
    """
        {% random_sites 5 as random_sites %}
    """
    return RandomSitesNode.handle_token(parser, token)
