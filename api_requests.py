import json
from urllib import request, parse

_PURECLOUD_API_BASE_URL = 'https://api.mypurecloud.com/api/v2'


def _get_endpoint_url(endpoint):
    return _PURECLOUD_API_BASE_URL + endpoint


def _get_response(r):
    return json.loads(r.read().decode('utf-8'))


def get(endpoint, token):
    req = request.Request(_get_endpoint_url(endpoint))
    req.add_header('Authorization', 'Bearer ' + token)
    resp = None
    with request.urlopen(req) as r:
        resp = _get_response(r)

    return resp


def post(endpoint, token, data):
    enc_data = parse.urlencode(data).encode()
    req = request.Request(_get_endpoint_url(endpoint), data=enc_data)
    req.add_header('Authorization', 'Bearer ' + token)
    resp = None
    with request.urlopen(req) as r:
        resp = _get_response(r)

    return resp
