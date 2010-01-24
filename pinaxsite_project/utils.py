from django import template



class AsNode(template.Node):
    
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
    
    def __init__(self, context_var):
        self.context_var = context_var