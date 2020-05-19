import requests
from urllib.parse import quote
from requests_oauthlib import OAuth1Session
from .etsy_env import EtsyEnvProduction

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
    def get_request_url_and_token_secret(api_key, shared_secret, permission_scopes=[], callback_uri=None, etsy_env=EtsyEnvProduction()):
        '''
        This method implements the first step of the Oauth1.0 3-legged work flow.

        Returns the  the login_url for the user you wish to authenticate with your app
        and the oauth_token_secret which must be passed to the get_oauth_token method
        (the next step in the oauth_workflow). You probably want to redirect the user
        to the login_url after this step.

        api_key is the keystring from etsy
        shared_secret is the shared secret from etsy
        permission_scopes is a list of strings. one string per requested permission scope. See link below.
            https://www.etsy.com/developers/documentation/getting_started/oauth#section_permission_scopes
        callback_uri is a path in your application where the user should be redirected after login
        etsy_env is always prod because there is only one etsy environment as of now
        '''
        oauth = OAuth1Session(api_key, client_secret=shared_secret, callback_uri=callback_uri)

        request_token_url = etsy_env.request_token_url
        if (permission_scopes):
            permissions = ' '.join(permission_scopes)
            request_token_url += '?scope=' + quote(permissions)

        request_token_response = oauth.fetch_request_token(request_token_url)

        login_url = request_token_response['login_url']
        temp_oauth_token_secret = request_token_response['oauth_token_secret']

        return (login_url, temp_oauth_token_secret)

    @staticmethod
    def get_oauth_token_via_auth_url(api_key, shared_secret, oauth_token_secret, auth_url, etsy_env=EtsyEnvProduction()):
        '''
        Retrieves the oauth_token and oauth_token_secret for the user. These are
        used along with the api_key, shared_secret, and oauth_token_secret (which
        is returned by get_request_url_and_token_secret) to create an EtsyOAuthClient.

        Differs from get_oauth_token_via_verifier as the auth_url containing the verifier and temp_oauth_token
        is passed in as a parameter. The auth_url is the url etsy redirected the user to after they allowed your app
        access to their data. It is the callback_url specified in get_request_url_and_token_secret with the query string
        etsy appended to it. This function will get the verifier and oauth_token from the auth_url query parameters.

        api_key is the keystring from etsy.
        shared_secret is the shared secret from etsy.
        oauth_token_secret is the token_secret returned from get_request_url_and_token_secret.
        auth_url is the url etsy redirected you to e.g. it is the callback url you specified
            in get_request_url_and_token_secret with the query string etsy appended to it.
        etsy_env is always prod because there is only one etsy environment as of now.
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

    @staticmethod
    def get_oauth_token_via_verifier(api_key, shared_secret, temp_oauth_token, temp_oauth_token_secret, verifier, etsy_env=EtsyEnvProduction()):
        '''
        Retrieves the oauth_token and oauth_token_secret for the user. These are
        used along with the api_key, shared_secret, and oauth_token_secret (which
        is returned by get_request_url_and_token_secret) to create an EtsyOAuthClient.

        Differs from get_oauth_token_via_auth_url as the temp_oauth_token and verifier are passed
        as params rather than retrieved from the auth_url. The temp_oauth_token is the oauth_token
        query string param from the login_url generated in get_request_url_and_token_secret.

        api_key is the keystring from etsy.
        shared_secret is the shared secret from etsy.
        temp_oauth_token is the oauth_token query string param from the login_url generated
            in get_request_url_and_token_secret.
        temp_oauth_token_secret is the token_secret returned from get_request_url_and_token_secret.
        verifier is the verification code on the page etsy redirects you to if no callback url
            was specified in get_request_url_and_token_secret.
        etsy_env is always prod because there is only one etsy environment as of now.
        '''
        oauth = OAuth1Session(api_key, shared_secret)
        oauth = OAuth1Session(api_key,
                  client_secret=shared_secret,
                  resource_owner_key=temp_oauth_token,
                  resource_owner_secret=temp_oauth_token_secret,
                  verifier=verifier)

        oauth_tokens = oauth.fetch_access_token(etsy_env.access_token_url)
        oauth_token = oauth_tokens['oauth_token']
        oauth_token_secret = oauth_tokens['oauth_token_secret']

        return (oauth_token, oauth_token_secret)
