"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


class AMMForm(FlaskForm):

    name = StringField(
        'AMM Market Name',
        default="Balancer",
        validators=[DataRequired()]
    )
    name_x = StringField(
        'Token X Name',
        default="ETH",
        validators=[DataRequired()]
    )
    weight_x = FloatField(
        'Token X Weight (Optional)',
        validators=[Optional()]
    )
    bal_x = FloatField(
        'Token X Balance',
        validators=[
            DataRequired()
        ]
    )
    name_y = StringField(
        'Token Y Name',
        default="DOUGH",
        validators=[DataRequired()]
    )
    bal_y = FloatField(
        'Token Y Balance',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Submit')
