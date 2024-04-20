from flask import Flask, redirect, request
from keycloak import KeycloakOpenID
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "F$$asE!iQ8a_mnthn"
app.config['KEYCLOAK_REALM'] = 'ToDoRealm'
app.config['KEYCLOAK_CLIENT_ID'] = '1'
app.config['KEYCLOAK_CLIENT_SECRET'] = 'V5zd8eWsmtmfLP7fuVr0sP9UH2oP9aaD'

keycloak_openid = KeycloakOpenID(server_url='http://localhost:8080/auth',
                                 client_id=app.config['KEYCLOAK_CLIENT_ID'],
                                 realm_name=app.config['KEYCLOAK_REALM'],
                                 client_secret_key=app.config['KEYCLOAK_CLIENT_SECRET'])


def protected_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if token:
            try:
                userinfo = keycloak_openid.userinfo(token)
                if userinfo:
                    return f(*args, **kwargs)
            except:
                pass

        # Check if the user is already authenticated
        if 'code' in request.args:
            return f(*args, **kwargs)

        # Redirect to the authentication URL
        redirect_uri = 'http://localhost:5000/protected'  # Change the port if necessary
        auth_url = keycloak_openid.auth_url(
            redirect_uri=redirect_uri,
            scope='openid'
        )
        return redirect(auth_url)

    return decorated


@app.route('/')
def index():
    return "L E O...."


@app.route('/protected')
@protected_route
def protected():
    return 'Pummy...'


if __name__ == "__main__":
    app.run(debug=True)
