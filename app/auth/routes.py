import requests

from flask import Flask, render_template, redirect, request, url_for, current_app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from app.auth.helpers import is_access_token_valid, is_id_token_valid
from app import db, login
from app.auth import bp
from app.models import User


APP_STATE = 'ApplicationState'


@login.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


@bp.route("/login")
def login():
    # get request params
    query_params = {'client_id': current_app.config["CLIENT_ID"],
                    'redirect_uri': current_app.config["REDIRECT_URI"],
                    'scope': "openid email profile",
                    'state': current_app.config["APP_STATE"],
                    'nonce': current_app.config["NONCE"],
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=current_app.config["AUTH_URI"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)


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
        current_app.config["TOKEN_URI"],
        headers=headers,
        data=query_params,
        auth=(current_app.config["CLIENT_ID"], current_app.config["CLIENT_SECRET"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    if not is_access_token_valid(access_token, current_app.config["ISSUER"]):
        return "Access token is invalid", 403

    if not is_id_token_valid(id_token, current_app.config["ISSUER"], current_app.config["CLIENT_ID"], current_app.config["NONCE"]):
        return "ID token is invalid", 403

    # Authorization flow successful, get userinfo and login user
    userinfo_response = requests.get(current_app.config["USERINFO_URI"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id=unique_id, username=user_name, email=user_email
    )

    if not User.query.filter_by(id=unique_id).first():
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for("main.index"))


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
