from crypt import methods
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import (
    EditProfileForm, EmptyForm,
    GrpcEndpointForm, GrpCurlForm
)

from app.models import User
from app.main import bp, git_manager, grpc_manager


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route("/", methods=["GET", "POST"])
def dinghy_grpc_tasks_landing_page():
    """Index page for grpc tasks"""
    grpc_new_endpoint_form = GrpcEndpointForm()
    grpc_submit_grpcurl = GrpCurlForm()
    all_current_endpoints = get_all_grpc_endpoints()

    if grpc_new_endpoint_form.validate_on_submit():
        grpc_endpoint = grpc_new_endpoint_form.grpc_endpoint.data
        grpc_port = grpc_new_endpoint_form.grpc_port.data
        grpc_protocol_git_repo = grpc_new_endpoint_form.grpc_protocol_git_repo.data

        return render_template(
            "submit_new_grpc_endpoint.html",
            grpc_endpoint=grpc_endpoint,
            grpc_port=grpc_port,
            grpc_protocol_git_repo=grpc_protocol_git_repo,
        )

    if grpc_submit_grpcurl.validate_on_submit():
        grpc_endpoint = grpc_submit_grpcurl.grpc_endpoint.data
        grpc_method = grpc_submit_grpcurl.grpc_method.data
        json_file_upload = grpc_submit_grpcurl.json_file_upload.data

        return render_template(
            "submit_grpcurl.html",
            grpc_endpoint=grpc_endpoint,
            grpc_method=grpc_method,
            json_file_upload=json_file_upload,
        )

    return render_template(
        "grpc.html",
        grpc_new_endpoint_form=grpc_new_endpoint_form,
        all_current_endpoints=all_current_endpoints,
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user,
                           form=form)
