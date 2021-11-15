from django import template

import orcidaccount.settings as settings

register = template.Library()


@register.inclusion_tag('login_button.html')
def orcid_loginbutton():

    return {}


@register.inclusion_tag('orcid_js.html')
def orcid_js():
    context = {
        "authorize_url": settings.ORCID_AUTHORIZATION_URL,
        "client_id": settings.ORCID_CLIENT_ID,
        "requested_scope": settings.REQUESTED_SCOPE,
        "redirect_uri": settings.REDIRECT_URI,
    }
    return context
