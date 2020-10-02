import flask
import json
import rauth


class OAuthProvider(object):

    def __init__(self, name, credentials):
        self._name = name
        self._client_id = credentials['client_id']
        self._client_secret = credentials['client_secret']

    @property
    def name(self):
        return self._name

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    def authorize(self):
        return NotImplementedError('OAuthProvider subclass needs to implement this method')

    def get_access_token(self, code):
        return NotImplementedError('OAuthProvider subclass needs to implement this method')

    def get_callback_url(self):
        return flask.url_for('oauth_callback', _external='http://localhost:5000')


def auth_response_decoder(response):
    return json.loads(response.decode('utf-8'))


class PureCloudOAuthProvider(OAuthProvider):

    BASE_URL = 'https://login.mypurecloud.com/'
    AUTHORIZE_URL = 'https://login.mypurecloud.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://login.mypurecloud.com/oauth/token'

    def __init__(self, credentials):
        super().__init__('purecloud', credentials)
        self._service = rauth.OAuth2Service(
            name=self.name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=self.AUTHORIZE_URL,
            access_token_url=self.ACCESS_TOKEN_URL,
            base_url=self.BASE_URL
        )

    def get_authorize_url(self):
        return self._service.get_authorize_url(
            response_type='code',
            redirect_uri=self.get_callback_url()
        )

    def authorize(self):
        return flask.redirect(self.get_authorize_url())

    def get_access_token(self, auth_code):
        token_req_data = {
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.get_callback_url()
        }
        oauth_session = self._service.get_auth_session(
            data=token_req_data, decoder=auth_response_decoder)
        return oauth_session.access_token
