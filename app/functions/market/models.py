"""Database models."""
from .. import db

class Market(db.Model):
    """Manage Market references."""
    __tablename__ = 'simulations'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    buy_volume = db.Column(
        db.float,
        nullable=True,
        unique=True
    )
    sell_volume = db.Column(
        db.true,
        nullable=True,
        unique=True
    )
    amms = db.relationship('AMM',
                            backref='simulation',
                            lazy=True)
    simulation_id = db.Column(
        db.Integer,
        db.ForeignKey('simulations.id'),
        nullable=False
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.address,
            'user_id': self.user_id,
            'amms': len(self.amms)
            }



# class SimSettings(db.Model):
#     __tablename__ = 'sim_settings'
#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )
#     seed_ = db.Column(
#         db.Integer,
#         primary_key=True
#     )
