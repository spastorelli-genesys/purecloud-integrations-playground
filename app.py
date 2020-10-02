import api_requests
import models
import oauth
import flask
import flask_login

app = flask.Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = b'\x93\xa6\xc0\r7N\xe2\xe6\xbe\xd0<do-v\xfc'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

_PURECLOUD_OAUTH_CREDS = {
    'client_id': 'xxxxxxxxxxxxxxxx',
    'client_secret': 'xxxxxxxxxxxxxxxx'
}
_PURECLOUD_OAUTH_PROVIDER = oauth.PureCloudOAuthProvider(
    _PURECLOUD_OAUTH_CREDS)

# For now user an in-memory Users Map.
# TODO: Use DB instead
_Users = {}


@login_manager.user_loader
def load_user(user_id):
    return _Users.get(user_id, None)


@app.route('/actions/customers/<id>', methods=['GET'])
def test_action(id):
    print('Received request for customer: ', id)
    return flask.json.jsonify({
        'id': id,
        'name': 'Joe Smith'
    })


@app.route('/oauth/callback')
def oauth_callback():
    cur_user = flask_login.current_user
    if not cur_user.is_anonymous:
        return flask.redirect(flask.url_for('home'))

    auth_code = flask.request.args.get('code', None)
    if not auth_code:
        return flask.redirect(flask.url_for('login'))

    access_token = _PURECLOUD_OAUTH_PROVIDER.get_access_token(auth_code)
    if not access_token:
        return flask.redirect(flask.url_for('login'))

    user_info = api_requests.get('/users/me?expand=organization', access_token)
    user_info['access_token'] = access_token

    # TODO: improve user retrieval/lookup
    global _Users
    user = models.User.from_user_info(user_info)
    _Users[user.id] = user

    flask_login.login_user(user)

    return flask.redirect(flask.url_for('home'))


@app.route('/login')
def login():
    cur_user = flask_login.current_user
    print(cur_user.is_active)
    if not cur_user.is_anonymous:
        return flask.redirect(flask.url_for('home'))

    context = {
        'page_title': 'Login',
        'purecloud_login_url': _PURECLOUD_OAUTH_PROVIDER.get_authorize_url()}
    return flask.render_template('login.html', **context)


@app.route('/webrtc')
@flask_login.login_required
def webrtc():
    context = {'page_title': 'WebRTC'}
    return flask.render_template('webrtc.html', **context)


@app.route('/screenshare-activation-code')
@flask_login.login_required
def screenshare_activation_code():
    context = {'page_title': 'Screenshare Activation Code'}
    return flask.render_template("screenshare_code.html", **context)


@app.route('/chat')
def chat():
    return flask.render_template('chat.html')


@app.route('/chat1')
def chat1():
    return flask.render_template('chat1.html')


@app.route('/chat2')
def chat2():
    return flask.render_template('chat2.html')


@app.route('/cobrowse')
def cobrowse():
    return flask.render_template('cobrowse.html')


@app.route('/')
def home():
    context = {'page_title': 'Home'}
    return flask.render_template('home.html', **context)
