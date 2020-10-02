import uuid
from collections import namedtuple

import flask_login

PureCloudOrg = namedtuple('PureCloudOrg', 'id name')


class User(flask_login.UserMixin):

    def __init__(self, username, access_token, name, email, purecloud_id, purecloud_org):
        self._id = str(uuid.uuid4())
        self._username = username
        self._access_token = access_token
        self._name = name
        self._email = email
        self._purecloud_id = purecloud_id
        self._purecloud_org = purecloud_org
        self._is_active = True

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def access_token(self):
        return self._access_token

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def purecloud_id(self):
        return self._purecloud_id

    @property
    def purecloud_org(self):
        return self._purecloud_org

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def set_is_active(self, active):
        self._is_active = active

    @staticmethod
    def from_user_info(user_info):
        purecloud_org = PureCloudOrg(
            user_info['organization']['id'], user_info['organization']['name'])
        return User(
            user_info['username'], user_info['access_token'],
            user_info['name'], user_info['email'], user_info['id'], purecloud_org
        )
