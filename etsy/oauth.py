import urllib
import requests
from requests_oauthlib import OAuth1Session
from etsy.etsy_env import EtsyEnvProduction

# TODO add support for generating the oauth credentials - may want to inherit from OAuth1Session
class EtsyOAuthClient():
    '''
    You must perform the oauth authentication on your own. This client
    expects valid oauth crendentials for the requesting user.

    client_key is keystring for the etsy app.
    client_secret is the shared secret for the etsy app.
    resource_owner_key is the oauth_token for the user whose data is being retrieved.
    resource_owner_secret is the oauth_token_secret for the user whose data is being retrieved.
    '''
    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret, logger=None):
        self.oauth1Session = OAuth1Session(client_key,
                                           client_secret=client_secret,
                                           resource_owner_key=resource_owner_key,
                                           resource_owner_secret=resource_owner_secret)
        self.logger = logger

    def do_oauth_request(self, url, http_method, data):
        # TODO data seems to work for PUT and POST /listing. See if data 
        # can handle image updates if so don't need to split path.
        if (http_method == "POST"):
            response = self.oauth1Session.request(http_method, url, files=data)
        else:
            response = self.oauth1Session.request(http_method, url, data=data)

        if self.logger:
            self.logger.debug('do_oauth_request: response = %r' % response)

        return response