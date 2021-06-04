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


class SimulationForm(FlaskForm):

    name = StringField(
        'Simulation Name',
        default="n/a",
    )
    days = IntegerField(
        'Days to Simulate',
        default=30,
        validators=[DataRequired()]
    )
    # _yield =
    submit = SubmitField('Submit')

class SimulationUpdateForm(FlaskForm):
    id = IntegerField(
        'ID',
        default=None,
    )
    name = StringField(
        'Simulation Name',
        default="n/a",
    )
    days = IntegerField(
        'Days to sim',
        default=30,
        validators=[DataRequired()]
    )
    # _yield =
    submit = SubmitField('Submit')

class ActionForm(FlaskForm):
    name = IntegerField(
        'Days to simulate',
        default=7,
        validators=[DataRequired()]
    )
    _daily_y_change = IntegerField(
        'Net Daily Y volume',
        default=40000,
        validators=[DataRequired()]
    )
    # _yield =


    submit = SubmitField('Submit')


class InitialLiquidityForm(FlaskForm):
    """User Log-in Form."""
    pool_name = StringField(
        'Sushi ETH Balance',
        validators=[
            DataRequired()
        ]
    )
    pool_x_weight = FloatField(
        'ETH Balance',
        default=0.5,
        validators=[
            DataRequired()
        ]
    )
    pool_x_balance = FloatField(
        'ETH Balance',
        validators=[
            DataRequired()
        ]
    )
    pool_y_balance = FloatField(
        'DOUGH Balance',
        validators=[
            DataRequired()
        ]
    )
