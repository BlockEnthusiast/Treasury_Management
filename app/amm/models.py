import math
# import matplotlib.pyplot as plt
import numpy as np
from ..simulator.models import Simulation
from .. import db

# To differentiate first and last from movement display
MARKER_FIRST = {
            'marker': "o",
            'markerfacecolor': "green",
            'markersize': "14",
            }
MARKER = {
            'marker': "x",
            'markerfacecolor': "yellow",
            'markersize': "10",
            }
MARKER_LAST = {
            'marker': "d",
            'markerfacecolor': "blue",
            'markersize': "14",
            }

class AMM(db.Model):
    """AMM model."""
    __tablename__ = 'amms'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
    )
    name_x = db.Column(
        db.String(10),
        nullable=False,
    )
    bal_x = db.Column(
        db.Float,
        default=0,
        nullable=False,
    )
    name_y = db.Column(
        db.String(10),
        nullable=False,
    )
    bal_y = db.Column(
        db.Float,
        default=0,
        nullable=False,
    )
    weight_x = db.Column(
        db.Float,
        default=0.5,
        nullable=False,
    )
    weight_y = db.Column(
        db.Float,
        default=0.5,
        nullable=False,
    )
    is_dynamic = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )
    records = db.relationship('AMM_Record',
                            backref='amm_records',
                            lazy=True)
    #
    simulation_id = db.Column(
        db.Integer,
        db.ForeignKey('simulations.id'),
        nullable=False
    )
    #
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_x': self.name_x,
            'bal_x': self.bal_x,
            'weight_x': self.weight_x,
            'name_y': self.name_y,
            'bal_y': self.bal_y,
            'weight_y': self.weight_y,
            'is_dynamic': self.is_dynamic,
            'simulation_id': self.simulation_id
            }
#
    def constant_product(self):
        return self.v() if self.is_dynamic else self.k()

    def k(self):
        return self.bal_x * self.bal_y
    #
    def v(self):
        return (self.bal_x ** self.weight_x) * (self.bal_y ** self.weight_y)
    #
    def x_price(self):
        return self._d_x_price() if self.is_dynamic else self._c_x_price()
    #
    def _c_x_price(self):
        return self.bal_y / self.bal_x
    #
    def _d_x_price(self):
        return (self.bal_y / self.weight_y) / (self.bal_x / self.weight_x)
    #
    def y_price(self):
        return self._d_y_price() if self.is_dynamic else self._c_y_price()
    #
    def _c_y_price(self):
        return self.bal_x / self.bal_y
    #
    def _d_y_price(self):
        return (self.bal_x / self.weight_x) / (self.bal_y / self.weight_y)
    #
    def seed(self, _x, _y):
        self.bal_x = _x
        self.bal_y = _y
        # self.clear_records()
    #
    def add_liquidity(self, _x):
        return self._d_add_liquidity(_x) if self.is_dynamic else self._c_add_liquidity(_x)
    #
    def _c_add_liquidity(self, _x):
        new_y = _x * self.bal_y / self.bal_x + 1
        self.bal_x += _x
        self.bal_y += new_y
        return
    #
    def _d_add_liquidity(self, _x):
        new_token = _x * self.bal_y / self.bal_x + 1
        self.bal_x += _x
        self.bal_y += new_token
        return
    #
    def apply_volume(self, _net_y_volume):
        self._d_apply_volume(_net_y_volume) if self.is_dynamic else self._c_apply_volume(_net_y_volume)
        return
    #
    def _c_apply_volume(self, _net_y_volume):
        if abs(_net_y_volume) >= self.bal_y:
            return False
        k = self.k()
        x = self.bal_x
        y = self.bal_y
        self.bal_x = k / (y + _net_y_volume)
        self.bal_y = y + _net_y_volume
        return True
    #
    def _d_apply_volume(self, _net_y_volume):
        if abs(_net_y_volume) >= self.bal_y:
            return False
        tokens_in, tokens_out, is_x_in = self._d_volume_math(_net_y_volume)
        if is_x_in:
            print(is_x_in)
            print("!!Tokens!!")
            print(tokens_in)
            print(tokens_out)
            print(_net_y_volume)
            self.bal_x += tokens_in
            self.bal_y -= tokens_out
        else:
            print("!!Reverse Tokens!!")
            print(tokens_in)
            print(tokens_out)
            self.bal_x += tokens_out
            self.bal_y -= tokens_in
        return True


    def _d_volume_math(self, _net_y_volume ):
        print(_net_y_volume)
        if _net_y_volume > 0:
            # Rename
            is_x_in = False
            amount_tokens_swapped_in = _net_y_volume
            bal_outgoing_token = self.bal_x
            bal_incoming_token = self.bal_y
            # Separate Concerns
            weight_factor = self.weight_y / self.weight_x
            incoming_factor = bal_incoming_token / (bal_incoming_token + amount_tokens_swapped_in)
            # Culmination
            amount_tokens_swapped_out = bal_outgoing_token * (1 - (incoming_factor ** weight_factor))
        else:
            # Rename
            is_x_in = True
            amount_tokens_swapped_out = _net_y_volume
            bal_outgoing_token = self.bal_y
            bal_incoming_token = self.bal_x
            # Separate Concerns
            weight_factor = self.weight_y / self.weight_x
            outgoing_factor = amount_tokens_swapped_out / bal_outgoing_token # = (1 - (incoming_factor ** weight_factor))
            incoming_factor = (1 - outgoing_factor)**(1/weight_factor)
            # Culmination
            amount_tokens_swapped_in = (bal_incoming_token / incoming_factor) - bal_incoming_token
        return amount_tokens_swapped_in, amount_tokens_swapped_out, is_x_in

    def set_weight_x(self, _weight):
        if _weight >= 1 or _weight <= 0:
            return False
        self.weight_x = _weight
        self.weight_y = 1 - _weight
        self.is_dynamic = True

    def plot_curve(self, _plotter):
        max_x = self.bal_x * 2
        max_y = self.bal_y * 2

        x, y, extras = self._d_plot_curve(_plotter) if self.is_dynamic else self._c_plot_curve(_plotter)

        _plotter.plot(x, y, extras)
        _plotter.set_limits(1, max_x, 1, max_y)
        _plotter.set_axis( "X Balance", "Y Balance")
        _plotter.set_title("{} Price Curve".format(self.name))
        return _plotter
    #
    def _c_plot_curve(self, _plotter):
        k = self.k()
        max_x = self.bal_x * 2
        interval = self.bal_x / 20
        x = np.arange(1, max_x, interval )
        y = k / x
        extras = {'label': "{} Price Curve".format(self.name),
                'color': 'black',
                'linestyle': 'dashed',
                'linewidth': 3,
                'marker': None,
                'markerfacecolor': None ,
                'markersize': None}
        return x, y, extras

    def _d_plot_curve(self, _plotter):
        v = self.v()
        max_x = self.bal_x * 2
        max_y = self.bal_y * 2
        interval = self.bal_x / 20
        x = np.arange(1, max_x, interval )
        y = (v / (x ** self.weight_x)) ** (1/self.weight_y)
        # (self.bal_x ** self.weight_x) * (self.bal_y ** self.weight_y)
        extras = {'label': "{} Price Curve".format(self.name),
                'color': 'black',
                'linestyle': 'dashed',
                'linewidth': '3',
                'marker': None,
                'markerfacecolor': None ,
                'markersize': None}
        return x, y, extras

    def plot_current(self):
        if first:
            marker = MARKER_FIRST
        elif last:
            marker = MARKER_LAST
        else:
            marker = MARKER
        extras = {'label': "{} Current Balance".format(self.name),
                'color': 'black',
                'linestyle': 'dashed',
                'linewidth': '3',
                'marker': marker['marker'],
                'markerfacecolor': marker['markerfacecolor'],
                'markersize': marker['markersize']}
        _plotter.plot(self.bal_x, self.bal_y, extras)
        return _plotter
    #
    def most_recent_record(self):
        records = self.records
        max_id = 0
        most_recent = None
        for record in records:
            if record.id > max_id:
                max_id = record.id
                most_recent = record
        return most_recent


#
class AMM_Record(db.Model):
    """AMM Historic Context model."""
    __tablename__ = 'amm_records'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    amm_id = db.Column(
        db.Integer,
        db.ForeignKey('amms.id'),
        nullable=False
    )
    token_price_x = db.Column(
        db.Float,
        nullable=False
    )
    bal_x = db.Column(
        db.Float,
        nullable=False
    )
    weight_x = db.Column(
        db.Float,
        nullable=False
    )
    token_price_y = db.Column(
        db.Float,
        nullable=False
    )
    bal_y = db.Column(
        db.Float,
        nullable=False
    )
    weight_y = db.Column(
        db.Float,
        nullable=False
    )
    constant_product = db.Column(
        db.Integer,
        nullable=False
    )
    @property
    def serialize(self):
        return {
            'id': self.id,
            'created_on': self.created_on,
            'amm_id': self.amm_id,
            'token_price_x': self.token_price_x,
            'bal_x': self.bal_x,
            'weight_x': self.weight_x,
            'token_price_y': self.token_price_y,
            'bal_y': self.bal_y,
            'weight_y': self.weight_y,
            'constant_product': self.constant_product
            }

    def plot_record(self, _plotter, first=False, last=False):
        if first:
            marker = MARKER_FIRST
        elif last:
            marker = MARKER_LAST
        else:
            marker = MARKER
        amm = AMM.query.get(self.amm_id)
        extras = {'label': "{} Current Balance".format(amm.name),
                'color': 'black',
                'linestyle': 'dashed',
                'linewidth': '3',
                'marker': marker['marker'],
                'markerfacecolor': marker['markerfacecolor'],
                'markersize': marker['markersize']}
        _plotter.plot(self.bal_x, self.bal_y, extras)
        return _plotter
