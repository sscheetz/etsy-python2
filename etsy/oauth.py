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
        # can handle image/actual file data updates if so don't need to split path.
        if (http_method == "POST"):
            response = self.oauth1Session.request(http_method, url, files=data)
        else:
            response = self.oauth1Session.request(http_method, url, data=data)

        if self.logger:
            self.logger.debug('do_oauth_request: response = %r' % response)

        return response

class EtsyOAuthHelper:
    '''
    Used to get the oauth token for the user you want to make requests with.
    TODO there might be a good way to make a class out of this, but because the
    methods are called in separate http requests the state would be lost in between
    calls.
    '''
    @staticmethod
    def get_request_url_and_token_secret(api_key, shared_secret, callback_uri=None, etsy_env=EtsyEnvProduction()):
        '''
        This method implements the first step of the Oauth1.0 3-legged work flow.
        
        Returns the  the login_url for the user you wish to authenticate with your app
        and the oauth_token_secret which must be passed to the get_oauth_token method
        (the next step in the oauth_workflow). You probably want to redirect the user
        to the login_url after this step.

        api_key is the keystring from etsy
        shared_secret is the shared secret from etsy
        callback_uri is a path in your application where the user should be redirected after login
        etsy_env is always prod because there is only one etsy environment as of now
        '''
        oauth = OAuth1Session(api_key, client_secret=shared_secret, callback_uri=callback_uri)

        request_token_response = oauth.fetch_request_token(etsy_env.request_token_url)
        
        login_url = request_token_response['login_url']
        temp_oauth_token_secret = request_token_response['oauth_token_secret']

        return (login_url, temp_oauth_token_secret)

    @staticmethod
    def get_oauth_token(api_key, shared_secret, oauth_token_secret, auth_url, etsy_env=EtsyEnvProduction()):
        '''
        Retrieves the oauth_token and oauth_token_secret for the user. These are 
        used along with the api_key, shared_secret, and oauth_token_secret (which
        is returned by get_request_url_and_token_secret) to create an EtsyOAuthClient.
        
        api_key is the keystring from etsy
        shared_secret is the shared secret from etsy
        oauth_token_secret is the token_secret returned from get_request_url_and_token_secret
        auth_url is the url used to start the current request. It is the callback_uri
            from get_request_url_and_token_secret with the extra parameters etsy appended
            to it after the user authenticated themselves.
        etsy_env is always prod because there is only one etsy environment as of now
        '''
        oauth = OAuth1Session(api_key, shared_secret)
        oauth_response = oauth.parse_authorization_response(auth_url)
        oauth = OAuth1Session(api_key,
                  client_secret=shared_secret,
                  resource_owner_key=oauth_response['oauth_token'],
                  resource_owner_secret=oauth_token_secret,
                  verifier=oauth_response['oauth_verifier'])
        
        oauth_tokens = oauth.fetch_access_token(etsy_env.access_token_url)
        oauth_token = oauth_tokens['oauth_token']
        oauth_token_secret = oauth_tokens['oauth_token_secret']

        return (oauth_token, oauth_token_secret)
