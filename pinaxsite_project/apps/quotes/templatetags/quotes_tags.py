from django import template

from quotes.models import Quote

from pinaxsite_project.utils import AsNode



register = template.Library()



class FeaturedQuoteNode(AsNode):
    
    def render(self, context):
        try:
            quote = Quote.objects.get(featured=True)
        except Quote.DoesNotExist:
            quote = None
        context[self.context_var] = quote


@register.tag
def featured_quote(parser, token):
    return FeaturedQuoteNode.handle_token(parser, token)
