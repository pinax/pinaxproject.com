from django import template

from biblion_extras.models import FeaturedPost

from pinaxsite_project.utils import AsNode



register = template.Library()



class FeaturedBlogPostNode(AsNode):
    
    def render(self, context):
        try:
            post = FeaturedPost.objects.select_related("post")[0].post
        except IndexError:
            post = None
        context[self.context_var] = post
        return u""


@register.tag
def featured_post(parser, token):
    return FeaturedBlogPostNode.handle_token(parser, token)
