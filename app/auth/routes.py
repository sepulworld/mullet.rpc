import requests

from flask import Flask, render_template, redirect, request, url_for, current_app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from app.auth.helpers import is_access_token_valid, is_id_token_valid, oauth_config
from app import db, login
from app.auth import bp
from app.models import User


APP_STATE = 'ApplicationState'
NONCE = 'SampleNonce'

@login.user_loader
def load_user(user_id):
    return User.get(user_id)


@bp.route("/login")
def login():
    # get request params
    query_params = {'client_id': oauth_config["client_id"],
                    'redirect_uri': oauth_config["redirect_uri"],
                    'scope': "openid email profile",
                    'state': current_app.config["APP_STATE"],
                    'nonce': current_app.config["NONCE"],
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=current_app.config["auth_uri"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)


@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@bp.route("/authorization-code/callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        oauth_config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(oauth_config["client_id"], oauth_config["client_secret"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    if not is_access_token_valid(access_token, oauth_config["issuer"]):
        return "Access token is invalid", 403

    if not is_id_token_valid(id_token, oauth_config["issuer"], oauth_config["client_id"], NONCE):
        return "ID token is invalid", 403

    # Authorization flow successful, get userinfo and login user
    userinfo_response = requests.get(oauth_config["userinfo_uri"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.query.filter_by(id=unique_id).first():
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for("profile"))


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
