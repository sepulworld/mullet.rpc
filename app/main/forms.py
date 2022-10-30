from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, SelectField, IntegerField
)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class GrpCurlForm(FlaskForm):
    """
    Form for grpcurl
    """

    grpc_endpoint = SelectField(
        "Grpcurl Endpoint Select",
        validators=[DataRequired()],
        # lookup choices from redis
    )

    grpc_method = StringField(
        "Grpcurl Method",
        validators=[DataRequired()],
        render_kw={"placeholder": "method"},
    )

    json_file_upload = FileField(
        "JSON File Upload. The file must be in JSON format, and can contain multiple JSON objects.",
        validators=[FileRequired(), FileAllowed(["json"], "JSON only!")],
    )

    submit = SubmitField("Grpcurl")


class GrpcEndpointForm(FlaskForm):
    """
    Form for grpcurl endpoint submission into available endpoints
    """

    grpc_endpoint = StringField(
        "Grpcurl Service Endpoint",
        validators=[DataRequired()],
        render_kw={"placeholder": "domain"},
    )

    grpc_port = IntegerField(
        "Grpcurl Port", validators=[DataRequired()], render_kw={"placeholder": "9090"}
    )

    grpc_protocol_git_repo = StringField(
        "Grpcurl Protocol Git Repo",
        validators=[DataRequired()],
        render_kw={"placeholder": "https://<git_repo_url>.git"},
    )

    submit = SubmitField("Grpcurl Endpoint")


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')



