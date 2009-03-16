from django import template

register = template.Library()
class ElswhereNetworks(template.Node):
    def __init__(self, user, result_var):
        self.user = template.Variable(user)
        self.result_var = result_var

    def render(self, context):
        try:
            actual_user = self.user.resolve(context)
            context[self.result_var] = actual_user.social_network_profiles.all()
        except template.VariableDoesNotExist:
            pass
        return ''
            
def do_elsewhere_networks(parser, token):
    """
    Retrieves a list of ``SocialNetworkProfile`` objects associated with 
    a given user and stores them in a context variable.

    Usage::

       {% elsewhere_networks [user] as [varname] %}

    Examples::

       {% elsewhere_networks request.user as user_networks %}

    """
    try:
        tag_name, user, as_string, result_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    return ElswhereNetworks(user, result_var)

register.tag('elsewhere_networks', do_elsewhere_networks)

