### App settings for Orcid Account Django App ###

# Authorization Url with ORCID
ORCID_AUTHORIZATION_URL = "https://sandbox.orcid.org/oauth/authorize"
# The requested scope
REQUESTED_SCOPE = "/read-limited" # If multiple scopes are desired, separate them with whitespaces
## Your Apps Client ID with ORCID
ORCID_CLIENT_ID = "" # Your Client ID from ORCID.org members API
## Your Apps secret wird ORCID
ORCID_CLIENT_SECRET = "" # Client Secret provided by ORCID.org members API
## Your Authentication langing page, as registered with ORCID
REDIRECT_URI = "<your base url>/accounts/auth" # redirect URI as registered with ORCID.org
## URL of ORCID-API to be used
ORCID_URL = "https://api.sandbox.orcid.org/v3.0/" # members API to be used
## URL for ORCID OAuth authentication
ORCID_OAUTH_URL = 'https://sandbox.orcid.org/oauth/token' # OAuth Authentication URL to be used
FROM_EMAIL = '' # The email adress from where your users shall receive notifications
IP_ADDRESS_HEADER = 'X-Forward-For' # The header where a user's IP Adress is stored. Default config for NGINX reverse proxy
