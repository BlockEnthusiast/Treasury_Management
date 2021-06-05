# from ..simulator.models import Simulation
from .. import db

#
class Address(db.Model):
    """AMM Historic Context model."""
    __tablename__ = 'addresses'
    address = db.Column(
        db.String,
        primary_key=True
    )
    liquidity_pools = db.relationship('LiquidityPool',
                            backref='address',
                            lazy=True)

    @property
    def serialize(self):
        return {
            'address': self.address,
            'liquidity_pools': len(self.liquidity_pools),
            }

class Token(db.Model):
    """Token model."""
    __tablename__ = 'tokens'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=True,
    )
    symbol = db.Column(
        db.String(100),
        nullable=True,
    )
    address = db.Column(
        db.String,
        db.ForeignKey('addresses.address'),
        nullable=False
    )
    logo = db.Column(
        db.String(100),
        nullable=True,
    )
    liquidity_pools = db.relationship('LiquidityPool',
                            backref='token',
                            lazy=True)
    # @property
    # def serialize(self):
    #     return {
    #         'address': self.address,
    #         'liquidity_pools': len(self.liquidity_pools),
    #         'amm_id': self.amm_id,
    #         'token_price_x': self.token_price_x,
    #         'bal_x': self.bal_x,
    #         'weight_x': self.weight_x,
    #         'token_price_y': self.token_price_y,
    #         'bal_y': self.bal_y,
    #         'weight_y': self.weight_y,
    #         'constant_product': self.constant_product
    #         }

class LiquidityPool(db.Model):
    """AMM Historic Context model."""
    __tablename__ = 'liquidity_pool'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    pair_address = db.Column(
        db.Integer,
        db.ForeignKey('addresses.address'),
        nullable=False
    )
    token_x_address = db.Column(
        db.Integer,
        db.ForeignKey('tokens.address'),
        nullable=False
    )
    token_y_address = db.Column(
        db.Integer,
        db.ForeignKey('tokens.address'),
        nullable=False
    )
    trends = db.relationship('Trend',
                            backref='liquidity_pool',
                            lazy=True)
    forecasts = db.relationship('Forecast',
                            backref='liquidity_pool',
                            lazy=True)
    # @property
    # def serialize(self):
    #     return {
    #         'address': self.address,
    #         'liquidity_pools': len(self.liquidity_pools),
    #         'amm_id': self.amm_id,
    #         'token_price_x': self.token_price_x,
    #         'bal_x': self.bal_x,
    #         'weight_x': self.weight_x,
    #         'token_price_y': self.token_price_y,
    #         'bal_y': self.bal_y,
    #         'weight_y': self.weight_y,
    #         'constant_product': self.constant_product
    #         }

class Trend(db.Model):
    """AMM Historic Context model."""
    __tablename__ = 'trends'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    liquidity_pool_id = db.Column(
        db.Integer,
        db.ForeignKey('liquidity_pools.id'),
        nullable=False
    )
    type = db.Column(
        db.String,
        nullable=False,
    )
    last_30_days = db.Column(
        db.Float,
        nullable=True,
    )
    last_14_days = db.Column(
        db.Float,
        nullable=True,
    )
    last_7_days = db.Column(
        db.Float,
        nullable=True,
    )
    today = db.Column(
        db.Float,
        nullable=True,
    )

    # @property
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'created_on': self.created_on,
    #         'amm_id': self.amm_id,
    #         'token_price_x': self.token_price_x,
    #         'bal_x': self.bal_x,
    #         'weight_x': self.weight_x,
    #         'token_price_y': self.token_price_y,
    #         'bal_y': self.bal_y,
    #         'weight_y': self.weight_y,
    #         'constant_product': self.constant_product
    #         }

class Forecast(db.Model):
    """Forecast model."""
    __tablename__ = 'forecasts'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    liquidity_pool_id = db.Column(
        db.Integer,
        db.ForeignKey('liquidity_pools.id'),
        nullable=False
    )
    next_30_day_total_return = db.Column(
        db.Float,
        nullable=True,
    )
    next_30_day_return_from_gov = db.Column(
        db.Float,
        nullable=True,
    )
    next_30_day_impermanent_loss = db.Column(
        db.Float,
        nullable=True,
    )
    next_30_day_return_from_fees = db.Column(
        db.Float,
        nullable=True,
    )
    equivalent_apr = db.Column(
        db.Float,
        nullable=True,
    )

    # @property
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'created_on': self.created_on,
    #         'amm_id': self.amm_id,
    #         'token_price_x': self.token_price_x,
    #         'bal_x': self.bal_x,
    #         'weight_x': self.weight_x,
    #         'token_price_y': self.token_price_y,
    #         'bal_y': self.bal_y,
    #         'weight_y': self.weight_y,
    #         'constant_product': self.constant_product
    #         }
